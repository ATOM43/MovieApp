from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from Movie import schemas, models
from datetime import datetime


def get_cinemaHall_by_id(db : Session, cinemaHall_id : int):
    return db.query(models.CinemaHall).filter(models.CinemaHall.id == cinemaHall_id).first()


def create(request : schemas.cinemaHall, db : Session ):
    new_cinemaHall = models.CinemaHall(name=request.name, 
                                        totalSeats=request.totalSeats, 
                                        cinema_id=request.cinema_id)                    
    db.add(new_cinemaHall)
    db.commit()
    db.refresh(new_cinemaHall)
    return new_cinemaHall

def get_all_cinemaHall(db: Session):    
    return db.query(models.CinemaHall).all()

def update(id: int, request: schemas.cinemaHall, db: Session):
    cinemaHall = db.query(models.ShowSeat).filter(models.ShowSeat.id == id)
    if not cinemaHall.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Booking with id {id} not found")
    cinemaHall.update(request.dict())
    db.commit()
    return 'updated'

def destroy(id: int,db: Session):
    cinemaHall = db.query(models.CinemaHall).filter(
            models.CinemaHall.id == id)
    if not cinemaHall.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Show Seat with {id} is not available")
    cinemaHall.delete(synchronize_session=False)
    db.commit()
    return 'Deleted'