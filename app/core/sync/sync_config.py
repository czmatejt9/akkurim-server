from app.features.athlete.schemas import AthleteReadPublic, AthleteStatusReadPublic
from app.features.trainer.schemas import TrainerReadPublic, TrainerStatusReadPublic

TABLE_NAMES = {
    "athlete": AthleteReadPublic,
    "athlete_status": AthleteStatusReadPublic,
    "trainer": TrainerReadPublic,
    "trainer_status": TrainerStatusReadPublic,
}
# TODO
