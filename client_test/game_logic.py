"""
    五子棋算法
"""


class GameLogic:
    def __init__(self):
        self.list = self.init_map_list()

    @staticmethod
    def init_map_list():
        """
            初始化游戏map
        """
        map = []
        for c in range(15):
            map_r = []
            for r in range(15):
                map_r.append(0)
            map.append(map_r)
        return map

    def win(self, row, line):

        if self.__crossrange(row, line) or self.__endwise(row, line) or self.__slant(row, line):
            return True
        else:
            return

    def __crossrange(self, row, line):
        """
            判断落点纵向棋子是否相同
        :param row: 横坐标
        :param line: 纵坐标
        :return:
        """
        color = self.list[row][line]

        positive = line + 1
        # 纵向负方向 棋盘坐标向下
        negative = line - 1
        # 纵向正方向 棋盘坐标向上
        count = 1
        while positive < 14:
            if self.list[row][positive] == color:
                count += 1
                positive += 1
            else:
                break
        while negative >= 0:
            if self.list[row][negative] == color:
                count += 1
                negative -= 1
            else:
                break
        return self.__judge_row(count, positive, negative, row)

    def __endwise(self, row, line):
        """
            判断落点横向棋子是否相同
        :param row:
        :param line:
        :return:
        """
        color = self.list[row][line]

        positive = row + 1
        # 横向正方向 棋盘坐标向右
        negative = row - 1
        # 横向负方向 棋盘坐标向左
        count = 1
        while positive < 15:
            if self.list[positive][line] == color:
                count += 1
                positive += 1
            else:
                break
        while negative >= 0:
            if self.list[negative][line] == color:
                count += 1
                negative -= 1
            else:
                break
        return self.__judge_line(count, positive, negative, line)

    def __slant(self, row, line):
        color = self.list[row][line]
        r_positive = row + 1
        # 横向正方向 棋盘坐标向右
        r_negative = row - 1
        # 横向负方向 棋盘坐标向左
        l_positive = line + 1
        # 纵向正方向 棋盘坐标向下
        l_negative = line - 1
        # 纵向负方向 棋盘坐标向上
        right_count = 1
        left_count = 1
        if self.__right_slant(r_negative, r_positive, l_positive, l_negative, color, right_count) or self.__left_slant(
                r_negative, r_positive, l_positive, l_negative, color, left_count):
            return True

    def __judge_row(self, count, positive, negative, row):
        if count == 5:
            return True
        elif count == 4:
            if positive < 14 and negative > 0:
                if self.list[row][positive + 1] == 0 and \
                        self.list[row][negative - 1] == 0:
                    return True
        else:
            return

    def __judge_line(self, count, positive, negative, line):
        if count == 5:
            return True
        elif count == 4:
            if positive < 14 and negative > 0:
                if self.list[positive + 1][line] == 0 and \
                        self.list[negative - 1][line] == 0:
                    return True
        else:
            return

    def __right_slant(self, r_negative, r_positive, l_positive, l_negative, color, right_count):
        """
             判断方向 ： 右斜线-->左上至右下
        :param r_negative:
        :param r_positive:
        :param l_positive:
        :param l_negative:
        :param color:
        :param right_count:
        :return:
        """

        while r_negative > 0 or l_negative >= 0:
            # 判断落点左上方向
            if self.list[r_negative][l_negative] == color:
                right_count += 1
                r_negative -= 1
                l_negative -= 1
            else:
                break

        while r_positive <= 14 or l_positive <= 14:
            # 判断落点右下方向
            if self.list[r_positive][l_positive] == color:
                right_count += 1
                r_positive += 1
                l_positive += 1
            else:
                break
        return self.__judge_right_slant(r_negative, r_positive, l_positive, l_negative, right_count)

    def __left_slant(self, r_negative, r_positive, l_positive, l_negative, color, left_count):
        """
            判断方向 ： 左斜线-->右上至左下
        :param r_negative:
        :param r_positive:
        :param l_positive:
        :param l_negative:
        :param color:
        :param left_count:
        :return:
        """
        while r_positive < 14 or l_negative >= 0:
            # 判断落点右上方向
            if self.list[r_positive][l_negative] == color:
                left_count += 1
                r_positive += 1
                l_negative -= 1
            else:
                break
        while r_negative >= 0 or l_positive <= 14:
            # 判断落点左下方向
            if self.list[r_negative][l_positive] == color:
                left_count += 1
                r_negative -= 1
                l_positive += 1
            else:
                break
        return self.__judge_left_slant(r_negative, r_positive, l_positive, l_negative, left_count)

    def __judge_right_slant(self, r_negative, r_positive, l_positive, l_negative, count):
        if count == 5:
            return True
        elif count == 4:
            if (r_negative >= 0 and r_positive < 14) or \
                    (l_negative >= 0 and l_positive < 14):
                if self.list[r_positive + 1][l_positive + 1] == 0 and \
                        self.list[r_negative - 1][l_negative - 1] == 0:
                    return True
        else:
            return

    def __judge_left_slant(self, r_negative, r_positive, l_positive, l_negative, count):
        if count == 5:
            return True
        elif count == 4:
            if (r_negative >= 0 and r_positive < 14) or \
                    (l_negative >= 0 and l_positive < 14):
                if self.list[r_positive + 1][l_negative - 1] == 0 and \
                        self.list[r_negative - 1][l_positive + 1] == 0:
                    return True
        else:
            return


if __name__ == '__main__':
    GameLogic()
