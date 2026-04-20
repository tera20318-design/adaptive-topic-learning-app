from __future__ import annotations

from .adapters import DocumentGroundingAdapter, IngestionAdapter, NormalizedPacketAdapter
from .document_grounding import document_packets_from_raw_documents
from .loader import (
    PacketLoadIssue,
    PacketLoadResult,
    SCHEMA_PATH,
    extract_packet_payload,
    load_normalized_packet_schema,
    load_normalized_source_packet,
    load_normalized_source_packets,
    validate_normalized_source_packet,
    validate_normalized_source_packet_collection,
)
from cleanroom_runtime.ingestion_boundary import normalize_source_packet, normalize_source_packets, packet_integrity_notes

__all__ = [
    "DocumentGroundingAdapter",
    "IngestionAdapter",
    "NormalizedPacketAdapter",
    "PacketLoadIssue",
    "PacketLoadResult",
    "SCHEMA_PATH",
    "document_packets_from_raw_documents",
    "extract_packet_payload",
    "load_normalized_packet_schema",
    "load_normalized_source_packet",
    "load_normalized_source_packets",
    "normalize_source_packet",
    "normalize_source_packets",
    "packet_integrity_notes",
    "validate_normalized_source_packet",
    "validate_normalized_source_packet_collection",
]


def prepare_live_lite_request(*args, **kwargs):
    from .runtime import prepare_live_lite_request as _impl

    return _impl(*args, **kwargs)


def execute_live_lite_request(*args, **kwargs):
    from .runtime import execute_live_lite_request as _impl

    return _impl(*args, **kwargs)


__all__.extend(["execute_live_lite_request", "prepare_live_lite_request"])
