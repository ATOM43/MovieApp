from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from Movie import schemas, models
from datetime import datetime
from sqlalchemy.sql import func
import re


def get_booking_by_id(db : Session, Booking_id : int):
    return db.query(models.Booking).filter(models.Booking.id == Booking_id).first()


def create(request : schemas.booking, db : Session, id: int ):
    new_booking = models.Booking(noOfseats=request.noOfseats,
                    timestamp = datetime.utcnow(),
                    status = request.status,
                    user_id = id,
                    show_id = request.show_id)                    
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    db.begin_nested()
    for seat_id in request.seat_ids:    
        
        show_seat = db.query(models.ShowSeat).\
            filter(models.ShowSeat.cinemaSeat_id == seat_id).first()
        
        if show_seat.status:
            db.rollback()
            destroy(new_booking.id,db)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"seat with id {seat_id} is already booked")
        else:
            show_seat.status = 1
            show_seat.booking_id = new_booking.id

    

    db.commit()
    total_amt = db.query(func.sum(models.ShowSeat.price).label('amount')).\
            filter(models.ShowSeat.booking_id == new_booking.id).all()
    
    print(total_amt[0].amount)

    payment = models.Payment(amount=total_amt[0].amount,
                    timestamp = datetime.utcnow(),
                    transaction_id = 11111,
                    booking_id = new_booking.id)  
    db.add(payment)
    db.commit()
    db.refresh(payment)


    return new_booking


def get_all_booking(db: Session):
    location = db.query(models.Booking).all()
    return location

def update(id: int, request: schemas.booking, db: Session):
    booking = db.query(models.Booking).filter(models.Booking.id == id)
    if not booking.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Booking with id {id} not found")
    booking.update(request.dict())
    db.commit()
    return 'updated'

def destroy(id: int,db: Session):
    booking = db.query(models.Booking).filter(
            models.Booking.id == id)
    if not booking.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Booking with {id} is not available")
    booking.delete(synchronize_session=False)
    db.commit()
    return 'Deleted'