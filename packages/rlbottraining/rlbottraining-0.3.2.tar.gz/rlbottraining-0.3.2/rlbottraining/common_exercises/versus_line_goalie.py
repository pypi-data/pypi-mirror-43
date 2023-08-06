from dataclasses import dataclass
from math import pi

from rlbot.utils.game_state_util import GameState, BoostState, BallState, CarState, Physics, Vector3, Rotator

from rlbottraining.common_exercises.common_base_exercises import StrikerExercise
from rlbottraining.rng import SeededRandomNumberGenerator
from rlbottraining.training_exercise import Playlist

@dataclass
class VersusLineGoalie(StrikerExercise):

    def make_game_state(self, rng: SeededRandomNumberGenerator) -> GameState:
        vel_mul = rng.uniform(1.0, 2.1)
        return GameState(
            ball=BallState(physics=Physics(
                location=Vector3(0, -1500, 100),
                velocity=Vector3(vel_mul * 480 * rng.uniform(-1, 1), vel_mul * -2000, 0),
                angular_velocity=Vector3(0, 0, 0))),
            cars={
                # Goalie
                0: CarState(
                    physics=Physics(
                        location=Vector3(0, -5000, 15),
                        rotation=Rotator(0, rng.uniform(-.1, .1), 0),
                        velocity=Vector3(0, 0, 0),
                        angular_velocity=Vector3(0, 0, 0)),
                    jumped=True,
                    double_jumped=True,
                    boost_amount=100),
                # Striker
                1: CarState(
                    physics=Physics(
                        location=Vector3(0, 0, 15),
                        rotation=Rotator(0, pi / 2, 0),
                        velocity=Vector3(0, 0, 0),
                        angular_velocity=Vector3(0, 0, 0)),
                    jumped=False,
                    double_jumped=False,
                    boost_amount=100),
            },
            boosts={i: BoostState(0) for i in range(34)},
        )

def make_default_playlist() -> Playlist:
    return [
        VersusLineGoalie('VersusLineGoalie'),
    ]
