from app.models import User, Wallet

def test_add_expence_success(db_session):
    #Arrange
    user=User(login="test")
    db_session.add(user)
    db_session.flush()
    wallet=Wallet(name="card",balance=200, user_id=user.id)
    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)
    
    #Act
    response=client.post(
        "/api/v1/operations/expense",
        json={"wallet_name":"card"}
    )