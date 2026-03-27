from fastapi import HTTPException

from ..schemas.events import (
    BubbleShowEvent,
    DevEventRequest,
    EmotionSetEvent,
    ModeSwitchEvent,
    MotionPlayEvent,
    MoveIntentEvent,
    PetEvent,
    WindowMoveEvent,
)


class BehaviorPolicyEngine:
    def build_manual_bubble_event(self, text: str, duration_ms: int, source: str = 'dev-control') -> BubbleShowEvent:
        return BubbleShowEvent(
            text=text,
            duration_ms=duration_ms,
            source=source,
        )

    def build_manual_event(self, request: DevEventRequest, source: str = 'dev-control') -> PetEvent:
        if request.type == 'bubble.show':
            if not request.text or not request.text.strip():
                raise HTTPException(status_code=422, detail='bubble.show 需要提供 text。')
            return BubbleShowEvent(
                text=request.text.strip(),
                duration_ms=request.duration_ms,
                motion=(request.motion.strip() if request.motion and request.motion.strip() else None),
                expression=(request.expression.strip() if request.expression and request.expression.strip() else None),
                graph=(request.graph.strip() if request.graph and request.graph.strip() else None),
                source=source,
            )

        if request.type == 'emotion.set':
            if not request.emotion or not request.emotion.strip():
                raise HTTPException(status_code=422, detail='emotion.set 需要提供 emotion。')
            return EmotionSetEvent(
                emotion=request.emotion.strip(),
                graph=(request.graph.strip() if request.graph and request.graph.strip() else None),
                source=source,
            )

        if request.type == 'motion.play':
            if not request.motion or not request.motion.strip():
                raise HTTPException(status_code=422, detail='motion.play 需要提供 motion。')
            return MotionPlayEvent(
                motion=request.motion.strip(),
                priority=request.priority,
                source=source,
            )

        if request.type == 'mode.switch':
            if not request.mode or not request.mode.strip():
                raise HTTPException(status_code=422, detail='mode.switch 需要提供 mode。')
            return ModeSwitchEvent(mode=request.mode.strip(), source=source)

        if request.type == 'move.intent':
            if not request.intent or not request.intent.strip():
                raise HTTPException(status_code=422, detail='move.intent 需要提供 intent。')
            return MoveIntentEvent(intent=request.intent.strip(), source=source)

        if request.type == 'window.move':
            return WindowMoveEvent(dx=request.dx, dy=request.dy, source=source)

        raise HTTPException(status_code=422, detail='不支持的事件类型。')
