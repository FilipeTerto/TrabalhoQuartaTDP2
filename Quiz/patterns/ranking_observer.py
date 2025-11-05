from abc import ABC, abstractmethod

# Observer abstrato
class Observer(ABC):
    @abstractmethod
    def update(self, user_id: str, score: int):
        pass

# Subject abstrato
class Subject(ABC):
    def __init__(self):
        self._observers = []

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self, user_id: str, score: int):
        for observer in self._observers:
            observer.update(user_id, score)

# Implementação concreta do observer para ranking
class RankingObserver(Observer):
    def __init__(self, db):
        self.db = db

    def update(self, user_id: str, score: int):
        # Busca nome do usuário
        user_data = self.db.users.find_one({"_id": ObjectId(user_id)})
        if not user_data:
            return

        # Atualiza ou insere no ranking
        self.db.ranking.update_one(
            {"users_id": user_id},
            {"$set": {"username": user_data["name"], "total_score": score}},
            upsert=True
        )
