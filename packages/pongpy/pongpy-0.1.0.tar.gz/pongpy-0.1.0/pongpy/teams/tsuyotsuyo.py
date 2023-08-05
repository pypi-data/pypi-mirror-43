from pongpy.interfaces.team import Team
from pongpy.models.game_info import GameInfo
from pongpy.models.state import State
from pongpy.models.pos import Pos


class TsuyotsuyoTeam(Team):

    prev_ball: Pos

    @property
    def name(self) -> str:
        return 'TsuyoTsuyo'

    def __init__(self):
        self.prev_ball = Pos(0, 0)

    def atk_action(self, info: GameInfo, state: State) -> int:
        my_pos = state.mine_team.atk_pos
        ball_pos = state.ball_pos
        delta = 2

        # 内側にある時は真ん中へ
        if state.is_right_side:
            if my_pos.x < ball_pos.x:
                return self.aim_to(my_pos, info.height // 2 + delta)
        else:
            if my_pos.x > ball_pos.x:
                return self.aim_to(my_pos, info.height // 2 + delta)

        diff_x = abs(my_pos.x - ball_pos.x)
        vec_y = ball_pos.y - self.prev_ball.y
        total_y = ball_pos.y + vec_y * diff_x

        if total_y % (info.height * 2) <= info.height:
            return self.aim_to(my_pos, total_y % info.height + delta) * info.atk_return_limit
        else:
            return self.aim_to(my_pos, info.height * 2 - total_y % (2 * info.height) + delta) * info.atk_return_limit

    def def_action(self, info: GameInfo, state: State) -> int:
        my_pos = state.mine_team.def_pos
        ball_pos = state.ball_pos

        # 内側にある時は真ん中へ
        if state.is_right_side:
            if my_pos.x < ball_pos.x:
                return self.aim_to(my_pos, info.height // 2)
        else:
            if my_pos.x > ball_pos.x:
                return self.aim_to(my_pos, info.height // 2)

        diff_x = abs(my_pos.x - ball_pos.x)
        vec_y = ball_pos.y - self.prev_ball.y
        total_y = + ball_pos.y + vec_y * diff_x

        # set pos
        self.prev_ball = ball_pos

        if total_y % (info.height * 2) <= info.height:
            return self.aim_to(my_pos, total_y % info.height) * info.def_return_limit
        else:
            return self.aim_to(my_pos, info.height * 2 - total_y % (2 * info.height)) * info.def_return_limit

    def aim_to(self, current_pos: Pos, target_y: int):
        diff = target_y - current_pos.y
        if diff < -1:
            return -1
        if diff < 1:
            return 0
        return 1
