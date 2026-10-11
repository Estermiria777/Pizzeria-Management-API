from database import SessionLocal, engine, Base
from models import PizzaSize, Crust, Flavor

def seed_database():
    # 1. Cria no banco todas as tabelas mapeadas no models.py que ainda não existem
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # 2. Popula Tamanhos
        if db.query(PizzaSize).count() == 0:
            sizes = [
                PizzaSize(name="Pequena", max_flavors=1, price=25.00),
                PizzaSize(name="Média", max_flavors=2, price=35.00),
                PizzaSize(name="Grande", max_flavors=3, price=48.00),
                PizzaSize(name="Família", max_flavors=4, price=60.00),
            ]
            db.add_all(sizes)

        # 3. Popula Bordas
        if db.query(Crust).count() == 0:
            crusts = [
                Crust(name="Tradicional", price=0.00),
                Crust(name="Catupiry", price=8.00),
                Crust(name="Cheddar", price=8.00),
                Crust(name="Chocolate", price=10.00),
            ]
            db.add_all(crusts)

        # 4. Popula Sabores
        if db.query(Flavor).count() == 0:
            flavors = [
                Flavor(name="Calabresa", description="Calabresa fatiada, cebola e azeitonas", category="Salgada"),
                Flavor(name="Mussarela", description="Mussarela, tomate e orégano", category="Salgada"),
                Flavor(name="Frango com Catupiry", description="Frango desfiado e cobertura de catupiry", category="Salgada"),
                Flavor(name="Quatro Queijos", description="Mussarela, provolone, parmesão e gorgonzola", category="Salgada"),
                Flavor(name="Brigadeiro", description="Chocolate ao leite com granulado", category="Doce"),
            ]
            db.add_all(flavors)

        db.commit()
        print(" Carga inicial de dados inserida com sucesso!")
    except Exception as e:
        db.rollback()
        print(f" Erro ao popular banco: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()