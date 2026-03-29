import asyncio
from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException

from ..schemas.events import (
    DevEventRequest,
    DevScenarioSummary,
    DevSequenceDispatchResponse,
    DevSequenceRequest,
    DevSequenceStepRequest,
    MotionPlayEvent,
    PetEvent,
    VPetStateSnapshot,
    WindowMoveEvent,
)
from .behavior_policy_engine import BehaviorPolicyEngine
from .event_bus import EventBus
from .vpet_state_store import VPetStateStore


@dataclass(frozen=True)
class DevScenarioDefinition:
    summary: DevScenarioSummary
    request: DevSequenceRequest


@dataclass(frozen=True)
class PreparedSequenceStep:
    delay_ms: int
    event: PetEvent
    wait_for: str | None
    wait_timeout_ms: int
    settle_ms: int


class DevSequenceOrchestrator:
    def __init__(
        self,
        event_bus: EventBus,
        behavior_policy_engine: BehaviorPolicyEngine,
        vpet_state_store: VPetStateStore,
    ) -> None:
        self._event_bus = event_bus
        self._behavior_policy_engine = behavior_policy_engine
        self._vpet_state_store = vpet_state_store
        self._active_tasks: set[asyncio.Task[None]] = set()
        self._scenario_catalog = self._build_scenario_catalog()

    def list_scenarios(self) -> list[DevScenarioSummary]:
        return [definition.summary for definition in self._scenario_catalog.values()]

    async def dispatch_sequence(self, request: DevSequenceRequest) -> DevSequenceDispatchResponse:
        sequence_name = (request.name or 'custom-sequence').strip() or 'custom-sequence'
        source = request.source.strip() or 'dev-sequence'
        prepared_steps = self._prepare_steps(request.steps, source=source, sequence_name=sequence_name)
        self._start_background_run(prepared_steps)
        return DevSequenceDispatchResponse(
            status='accepted',
            sequence_name=sequence_name,
            step_count=len(prepared_steps),
            source=source,
        )

    async def dispatch_scenario(self, scenario_id: str) -> DevSequenceDispatchResponse:
        scenario_request = self._build_scenario_request(scenario_id)
        return await self.dispatch_sequence(scenario_request)

    def _build_scenario_request(self, scenario_id: str) -> DevSequenceRequest:
        key = scenario_id.strip().lower()
        definition = self._scenario_catalog.get(key)
        if definition is None:
            raise HTTPException(status_code=404, detail='未知组合场景。')
        return definition.request.model_copy(deep=True)

    def _build_scenario_catalog(self) -> dict[str, DevScenarioDefinition]:
        definitions = [
            self._create_definition(
                scenario_id='move-then-bubble',
                title='move -> bubble',
                description='先显式位移，再进入说话态。',
                steps=[
                    DevSequenceStepRequest(
                        event=DevEventRequest(type='window.move', dx=120, dy=-20),
                        wait_for='move_complete',
                    ),
                    DevSequenceStepRequest(
                        event=DevEventRequest(
                            type='bubble.show',
                            text='我先挪一下再说。',
                            duration_ms=5000,
                            expression='thinking',
                            graph='think',
                        ),
                    ),
                ],
            ),
            self._create_definition(
                scenario_id='bubble-then-move',
                title='bubble -> move',
                description='先说话，再做窗口位移，观察气泡与移动并存。',
                steps=[
                    DevSequenceStepRequest(
                        event=DevEventRequest(
                            type='bubble.show',
                            text='我边说边换位置。',
                            duration_ms=5000,
                            motion='touch_body',
                            expression='shy',
                        ),
                    ),
                    DevSequenceStepRequest(
                        event=DevEventRequest(type='window.move', dx=-120, dy=20),
                        wait_for='move_complete',
                    ),
                ],
            ),
            self._create_definition(
                scenario_id='move-then-motion',
                title='move -> motion',
                description='先位移，再切到单独动作。',
                steps=[
                    DevSequenceStepRequest(
                        event=DevEventRequest(type='window.move', dx=140, dy=0),
                        wait_for='move_complete',
                    ),
                    DevSequenceStepRequest(
                        event=DevEventRequest(type='motion.play', motion='touch_head', priority=50),
                    ),
                ],
            ),
            self._create_definition(
                scenario_id='move-then-bubble-touch',
                title='move -> bubble.touch',
                description='先位移，再进入原生触摸编排说话。',
                steps=[
                    DevSequenceStepRequest(
                        event=DevEventRequest(type='window.move', dx=-120, dy=0),
                        wait_for='move_complete',
                    ),
                    DevSequenceStepRequest(
                        event=DevEventRequest(
                            type='bubble.show',
                            text='move then touch bubble',
                            duration_ms=5000,
                            motion='touch_body',
                            expression='shy',
                        ),
                    ),
                ],
            ),
            self._create_definition(
                scenario_id='thinking-walk-think',
                title='think -> move -> speak',
                description='进入思考态后位移，再用 think graph 说话，验证更长链路状态切换。',
                steps=[
                    DevSequenceStepRequest(
                        event=DevEventRequest(type='mode.switch', mode='thinking'),
                        wait_for='event_applied',
                    ),
                    DevSequenceStepRequest(
                        event=DevEventRequest(type='window.move', dx=90, dy=-20),
                        wait_for='move_complete',
                        wait_timeout_ms=5000,
                        settle_ms=120,
                    ),
                    DevSequenceStepRequest(
                        event=DevEventRequest(
                            type='bubble.show',
                            text='我先想一下，再边移动边回答。',
                            duration_ms=5000,
                            expression='thinking',
                            graph='think',
                        ),
                    ),
                    DevSequenceStepRequest(
                        event=DevEventRequest(type='mode.switch', mode='normal'),
                    ),
                ],
            ),
            self._create_definition(
                scenario_id='bubble-move-touch-recover',
                title='bubble -> move -> touch -> normal',
                description='先说话，再位移，接一个触摸动作，最后回到 normal，验证恢复链路。',
                steps=[
                    DevSequenceStepRequest(
                        event=DevEventRequest(
                            type='bubble.show',
                            text='这次我连续做四步给你看。',
                            duration_ms=5000,
                            expression='shy',
                        ),
                        wait_for='event_applied',
                    ),
                    DevSequenceStepRequest(
                        event=DevEventRequest(type='window.move', dx=-110, dy=20),
                        wait_for='move_complete',
                        wait_timeout_ms=5000,
                        settle_ms=120,
                    ),
                    DevSequenceStepRequest(
                        event=DevEventRequest(type='motion.play', motion='touch_head', priority=55),
                        wait_for='motion_complete',
                        wait_timeout_ms=6000,
                        settle_ms=120,
                    ),
                    DevSequenceStepRequest(
                        event=DevEventRequest(type='mode.switch', mode='normal'),
                    ),
                ],
            ),
            self._create_definition(
                scenario_id='think-speak-move-touch-speak-recover',
                title='think -> speak -> move -> touch -> speak -> normal',
                description='更长的 6 步 story sequence，用于验证重复事件类型下的事件关联字段和完成门控。',
                steps=[
                    DevSequenceStepRequest(
                        event=DevEventRequest(type='mode.switch', mode='thinking'),
                        wait_for='event_applied',
                    ),
                    DevSequenceStepRequest(
                        event=DevEventRequest(
                            type='bubble.show',
                            text='我先想一下这件事。',
                            duration_ms=4000,
                            expression='thinking',
                            graph='think',
                        ),
                        wait_for='event_applied',
                    ),
                    DevSequenceStepRequest(
                        event=DevEventRequest(type='window.move', dx=80, dy=-20),
                        wait_for='move_complete',
                        wait_timeout_ms=5000,
                        settle_ms=120,
                    ),
                    DevSequenceStepRequest(
                        event=DevEventRequest(type='motion.play', motion='touch_head', priority=55),
                        wait_for='motion_complete',
                        wait_timeout_ms=6000,
                        settle_ms=120,
                    ),
                    DevSequenceStepRequest(
                        event=DevEventRequest(
                            type='bubble.show',
                            text='想好了，我继续说给你听。',
                            duration_ms=5000,
                            expression='thinking',
                            graph='think',
                        ),
                        wait_for='event_applied',
                    ),
                    DevSequenceStepRequest(
                        event=DevEventRequest(type='mode.switch', mode='normal'),
                    ),
                ],
            ),
        ]
        return {definition.summary.scenario_id: definition for definition in definitions}

    def _create_definition(
        self,
        scenario_id: str,
        title: str,
        description: str,
        steps: list[DevSequenceStepRequest],
    ) -> DevScenarioDefinition:
        return DevScenarioDefinition(
            summary=DevScenarioSummary(
                scenario_id=scenario_id,
                title=title,
                description=description,
                step_count=len(steps),
            ),
            request=DevSequenceRequest(
                name=scenario_id,
                source='dev-scenario',
                steps=steps,
            ),
        )

    def _prepare_steps(
        self,
        steps: list[DevSequenceStepRequest],
        source: str,
        sequence_name: str,
    ) -> list[PreparedSequenceStep]:
        prepared_steps: list[PreparedSequenceStep] = []
        for index, step in enumerate(steps):
            event = self._behavior_policy_engine.build_manual_event(step.event, source=source)
            event = self._attach_step_metadata(event, sequence_name=sequence_name, step_index=index)
            self._validate_wait_for(step, event)
            prepared_steps.append(
                PreparedSequenceStep(
                    delay_ms=step.delay_ms,
                    event=event,
                    wait_for=step.wait_for,
                    wait_timeout_ms=step.wait_timeout_ms,
                    settle_ms=step.settle_ms,
                )
            )
        return prepared_steps

    def _attach_step_metadata(self, event: PetEvent, sequence_name: str, step_index: int) -> PetEvent:
        event_id = event.event_id or f'{event.source}-{uuid4().hex[:12]}'
        return event.model_copy(
            update={
                'event_id': event_id,
                'sequence_name': sequence_name,
                'step_index': step_index,
            }
        )

    def _validate_wait_for(self, step: DevSequenceStepRequest, event: PetEvent) -> None:
        if step.wait_for == 'move_complete' and not isinstance(event, WindowMoveEvent):
            raise HTTPException(status_code=422, detail='wait_for=move_complete 只能用于 window.move。')
        if step.wait_for == 'motion_complete' and not isinstance(event, MotionPlayEvent):
            raise HTTPException(status_code=422, detail='wait_for=motion_complete 只能用于 motion.play。')

    def _start_background_run(self, prepared_steps: list[PreparedSequenceStep]) -> None:
        task = asyncio.create_task(self._run_sequence(prepared_steps))
        self._active_tasks.add(task)
        task.add_done_callback(self._active_tasks.discard)

    async def _run_sequence(self, prepared_steps: list[PreparedSequenceStep]) -> None:
        for step in prepared_steps:
            if step.delay_ms > 0:
                await asyncio.sleep(step.delay_ms / 1000)

            dispatched_at = datetime.now(timezone.utc)
            baseline_state = self._vpet_state_store.get_latest()
            await self._event_bus.publish(step.event)
            await self._wait_for_step(step, baseline_state, dispatched_at)

    async def _wait_for_step(
        self,
        step: PreparedSequenceStep,
        baseline_state: VPetStateSnapshot | None,
        dispatched_at: datetime,
    ) -> None:
        if not step.wait_for:
            return

        if step.wait_for == 'event_applied':
            await self._wait_for_event_applied(
                event=step.event,
                dispatched_at=dispatched_at,
                timeout_ms=step.wait_timeout_ms,
            )
        elif step.wait_for == 'move_complete':
            await self._wait_for_move_complete(
                event=step.event,
                baseline_state=baseline_state,
                dispatched_at=dispatched_at,
                timeout_ms=step.wait_timeout_ms,
            )
        elif step.wait_for == 'motion_complete':
            await self._wait_for_motion_complete(
                event=step.event,
                dispatched_at=dispatched_at,
                timeout_ms=step.wait_timeout_ms,
            )

        if step.settle_ms > 0:
            await asyncio.sleep(step.settle_ms / 1000)

    async def _wait_for_event_applied(
        self,
        event: PetEvent,
        dispatched_at: datetime,
        timeout_ms: int,
    ) -> VPetStateSnapshot:
        def predicate(state: VPetStateSnapshot | None) -> bool:
            return self._state_has_applied_event(state, event, dispatched_at)

        return await self._poll_state(
            predicate=predicate,
            timeout_ms=timeout_ms,
            error_detail=f'等待 {event.type} 被 VPet 消费超时。',
        )

    async def _wait_for_move_complete(
        self,
        event: PetEvent,
        baseline_state: VPetStateSnapshot | None,
        dispatched_at: datetime,
        timeout_ms: int,
    ) -> VPetStateSnapshot:
        if not isinstance(event, WindowMoveEvent):
            raise HTTPException(status_code=422, detail='move_complete 只能用于 window.move。')

        tolerance = 6.0
        expected_left = baseline_state.left + event.dx if baseline_state is not None else None
        expected_top = baseline_state.top + event.dy if baseline_state is not None else None

        def predicate(state: VPetStateSnapshot | None) -> bool:
            if not self._state_has_applied_event(state, event, dispatched_at):
                return False
            if state is None or expected_left is None or expected_top is None:
                return True
            return (
                abs(state.left - expected_left) <= tolerance
                and abs(state.top - expected_top) <= tolerance
            )

        return await self._poll_state(
            predicate=predicate,
            timeout_ms=timeout_ms,
            error_detail='等待 window.move 完成并落到目标位置超时。',
        )

    async def _wait_for_motion_complete(
        self,
        event: PetEvent,
        dispatched_at: datetime,
        timeout_ms: int,
    ) -> VPetStateSnapshot:
        if not isinstance(event, MotionPlayEvent):
            raise HTTPException(status_code=422, detail='motion_complete 只能用于 motion.play。')

        await self._wait_for_event_applied(
            event=event,
            dispatched_at=dispatched_at,
            timeout_ms=timeout_ms,
        )

        motion_key = self._normalize_state_token(event.motion)
        saw_motion_display = False

        def predicate(state: VPetStateSnapshot | None) -> bool:
            nonlocal saw_motion_display
            if not self._state_has_applied_event(state, event, dispatched_at):
                return False
            if self._state_matches_motion(state, motion_key):
                saw_motion_display = True
                return False
            return saw_motion_display

        return await self._poll_state(
            predicate=predicate,
            timeout_ms=timeout_ms,
            error_detail=f'等待 motion.play({event.motion}) 结束超时。',
        )

    async def _poll_state(self, predicate, timeout_ms: int, error_detail: str) -> VPetStateSnapshot:
        loop = asyncio.get_running_loop()
        deadline = loop.time() + (timeout_ms / 1000)
        while True:
            state = self._vpet_state_store.get_latest()
            if predicate(state):
                return state
            if loop.time() >= deadline:
                raise HTTPException(status_code=504, detail=error_detail)
            await asyncio.sleep(0.05)

    def _state_has_applied_event(
        self,
        state: VPetStateSnapshot | None,
        event: PetEvent,
        dispatched_at: datetime,
    ) -> bool:
        if state is None or state.last_event_at is None or state.last_event_at < dispatched_at:
            return False

        if event.event_id:
            return state.last_event_id == event.event_id

        return (
            state.last_event_type == event.type
        )

    def _state_matches_motion(self, state: VPetStateSnapshot | None, motion_key: str) -> bool:
        if state is None:
            return False
        display_name = self._normalize_state_token(state.display_name)
        display_type = self._normalize_state_token(state.display_type)
        return motion_key in {display_name, display_type}

    def _normalize_state_token(self, value: str | None) -> str:
        if not value:
            return ''
        return value.strip().lower().replace('-', '_').replace(' ', '_')
