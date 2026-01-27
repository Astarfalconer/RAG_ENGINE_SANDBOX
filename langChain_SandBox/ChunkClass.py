from dataclasses import dataclass, field    

@dataclass
class ChunkClass:
    chunk_id: str
    content: str
    page: int
    source: str





def CreateChunk(chunk_id: str, content: str, page: int, source: str) -> ChunkClass:
    return ChunkClass(
        chunk_id=chunk_id,
        content=content,
        page=page,
        source=source
    )   