import asyncio

from fastapi import HTTPException

from ..schemas.events import (
    DevEventRequest,
    DevScenarioSummary,
    DevSequenceDispatchResponse,
    DevSequenceRequest,
    DevSequenceStepRequest,
    PetEvent,
)
from .behavior_policy_engine import BehaviorPolicyEngine
from .event_bus import EventBus


class DevSequenceOrchestrator:
    def __init__(self, event_bus: EventBus, behavior_policy_engine: BehaviorPolicyEngine) -> None:
        self._event_bus = event_bus
        self._behavior_policy_engine = behavior_policy_engine
        self._active_tasks: set[asyncio.Task[None]] = set()

    def list_scenarios(self) -> list[DevScenarioSummary]:
        return [
            DevScenarioSummary(
                scenario_id='move-then-bubble',
                title='move -> bubble',
                description='先显式位移，再进入说话态。',
                step_count=2,
            ),
            DevScenarioSummary(
                scenario_id='bubble-then-move',
                title='bubble -> move',
                description='先说话，再做窗口位移，观察气泡与移动并存。',
                step_count=2,
            ),
            DevScenarioSummary(
                scenario_id='move-then-motion',
                title='move -> motion',
                description='先位移，再切到单独动作。',
                step_count=2,
            ),
            DevScenarioSummary(
                scenario_id='move-then-bubble-touch',
                title='move -> bubble.touch',
                description='先位移，再进入原生触摸编排说话。',
                step_count=2,
            ),
        ]

    async def dispatch_sequence(self, request: DevSequenceRequest) -> DevSequenceDispatchResponse:
        sequence_name = (request.name or 'custom-sequence').strip() or 'custom-sequence'
        source = request.source.strip() or 'dev-sequence'
        prepared_steps = self._prepare_steps(request.steps, source=source)
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
        if key == 'move-then-bubble':
            return DevSequenceRequest(
                name='move-then-bubble',
                source='dev-scenario',
                steps=[
                    DevSequenceStepRequest(
                        event=DevEventRequest(type='window.move', dx=120, dy=-20),
                    ),
                    DevSequenceStepRequest(
                        delay_ms=450,
                        event=DevEventRequest(
                            type='bubble.show',
                            text='我先挪一下再说。',
                            duration_ms=5000,
                            expression='thinking',
                            graph='think',
                        ),
                    ),
                ],
            )

        if key == 'bubble-then-move':
            return DevSequenceRequest(
                name='bubble-then-move',
                source='dev-scenario',
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
                        delay_ms=280,
                        event=DevEventRequest(type='window.move', dx=-120, dy=20),
                    ),
                ],
            )

        if key == 'move-then-motion':
            return DevSequenceRequest(
                name='move-then-motion',
                source='dev-scenario',
                steps=[
                    DevSequenceStepRequest(
                        event=DevEventRequest(type='window.move', dx=140, dy=0),
                    ),
                    DevSequenceStepRequest(
                        delay_ms=280,
                        event=DevEventRequest(type='motion.play', motion='touch_head', priority=50),
                    ),
                ],
            )

        if key == 'move-then-bubble-touch':
            return DevSequenceRequest(
                name='move-then-bubble-touch',
                source='dev-scenario',
                steps=[
                    DevSequenceStepRequest(
                        event=DevEventRequest(type='window.move', dx=-120, dy=0),
                    ),
                    DevSequenceStepRequest(
                        delay_ms=450,
                        event=DevEventRequest(
                            type='bubble.show',
                            text='move then touch bubble',
                            duration_ms=5000,
                            motion='touch_body',
                            expression='shy',
                        ),
                    ),
                ],
            )

        raise HTTPException(status_code=404, detail='未知组合场景。')

    def _prepare_steps(self, steps: list[DevSequenceStepRequest], source: str) -> list[tuple[int, PetEvent]]:
        prepared_steps: list[tuple[int, PetEvent]] = []
        for step in steps:
            event = self._behavior_policy_engine.build_manual_event(step.event, source=source)
            prepared_steps.append((step.delay_ms, event))
        return prepared_steps

    def _start_background_run(self, prepared_steps: list[tuple[int, PetEvent]]) -> None:
        task = asyncio.create_task(self._run_sequence(prepared_steps))
        self._active_tasks.add(task)
        task.add_done_callback(self._active_tasks.discard)

    async def _run_sequence(self, prepared_steps: list[tuple[int, PetEvent]]) -> None:
        for delay_ms, event in prepared_steps:
            if delay_ms > 0:
                await asyncio.sleep(delay_ms / 1000)
            await self._event_bus.publish(event)
