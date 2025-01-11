"""SampleItem base use case."""
from app.application.dto.sample_item import SampleItemReadDto
from app.domain.entities.sample_item import SampleItem


class SampleItemUseCaseBase:
    """SampleItem base use case."""

    def _to_return_dto(self, entity: SampleItem) -> SampleItemReadDto:
        return SampleItemReadDto.model_validate(entity)
