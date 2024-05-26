from fastapi import FastAPI, Depends

from sqlmodel import Session, select
from app.db import init_db, get_session
from app.models import Song, SongCreate, SongBase  # noqa

app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/ping")
async def pong():
    return {"ping": "pong!"}


@app.get("/songs", response_model=list[Song])
def get_songs(session: Session = Depends(get_session)):
    result = session.execute(select(Song))
    songs: [Song] = result.scalars().all()
    return [
        Song(
            id=song.id,
            name=song.name,
            artist=song.artist
        )
        for song in songs
    ]


@app.post("/songs")
def add_song(song: SongBase, session: Session = Depends(get_session)):
    song = Song(
        name=song.name,
        artist=song.artist
    )
    session.add(song)
    session.commit()
    session.refresh(song)
    return song
