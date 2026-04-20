from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol

from cleanroom_runtime.models import RunRequest, SourcePacket

from .document_grounding import document_packets_from_raw_documents
from .loader import PacketLoadResult, load_normalized_source_packets


class IngestionAdapter(Protocol):
    adapter_name: str

    def collect(self, request: RunRequest) -> list[SourcePacket]:
        ...


class DocumentGroundingAdapter:
    adapter_name = "document_grounding"

    def collect(self, request: RunRequest) -> list[SourcePacket]:
        return document_packets_from_raw_documents(request.raw_documents)


@dataclass(slots=True)
class NormalizedPacketAdapter:
    payload: Any
    adapter_name: str = "live_lite_loader"
    as_of_date: str = ""
    last_result: PacketLoadResult | None = field(default=None, init=False)

    def collect(self, request: RunRequest) -> list[SourcePacket]:
        result = load_normalized_source_packets(
            self.payload,
            adapter_name=self.adapter_name,
            as_of_date=request.as_of_date or self.as_of_date,
        )
        self.last_result = result
        return result.packets


__all__ = ["DocumentGroundingAdapter", "IngestionAdapter", "NormalizedPacketAdapter"]
