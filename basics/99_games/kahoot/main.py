import asyncio
import time
from typing import Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# ── How many questions the game actually plays ──
# Lower this (e.g. to 5) for a short warm-up round.
QUESTION_LIMIT = 20

ALL_QUESTIONS = [
    # ═══════════ LISTS — lesson 13 / topic 16 ═══════════
    # ── 1. len + index, first cell is 0 ──
    {
        "question": "What does this code print?",
        "code_hint": "nums = [8, 3, 14, 5, 20]\nprint(len(nums), nums[0], nums[2])",
        "options": [
            "5 8 14",
            "5 8 5",
            "4 8 14",
            "5 3 5",
        ],
        "correct": 0,
    },
    # ── 2. negative indexing ──
    {
        "question": "What is printed?",
        "code_hint": "colors = ['red', 'blue', 'green', 'pink']\nprint(colors[-1], colors[-3])",
        "options": [
            "red blue",
            "pink green",
            "pink blue",
            "Error — an index cannot be negative",
        ],
        "correct": 2,
    },
    # ── 3. slicing: the end is NOT included ──
    {
        "question": "What is printed?",
        "code_hint": "n = [10, 11, 12, 13, 14, 15, 16, 17]\nprint(n[2:5])",
        "options": [
            "[12, 13, 14, 15]",
            "[12, 13, 14]",
            "[11, 12, 13, 14]",
            "[10, 11]",
        ],
        "correct": 1,
    },
    # ── 4. slicing with a missing start / missing end ──
    {
        "question": "What are the two printed lists?",
        "code_hint": "n = [10, 11, 12, 13, 14, 15, 16, 17]\nprint(n[:4])\nprint(n[5:])",
        "options": [
            "[10, 11, 12, 13, 14]  then  [16, 17]",
            "[10, 11, 12, 13]  then  [15, 16, 17]",
            "[10, 11, 12, 13]  then  [16, 17]",
            "[11, 12, 13, 14]  then  [15, 16, 17]",
        ],
        "correct": 1,
    },
    # ── 5. slicing with a step ──
    {
        "question": "What is printed?",
        "code_hint": "n = [10, 11, 12, 13, 14, 15, 16, 17]\nprint(n[1::2])",
        "options": [
            "[10, 12, 14, 16]",
            "[11, 13, 15, 17]",
            "[11, 12, 13]",
            "[10, 11, 12, 13]",
        ],
        "correct": 1,
    },
    # ── 6. [::-1] reverses — it does NOT sort ──
    {
        "question": "What is printed?",
        "code_hint": "sizes = [2, 7, 4, 9]\nprint(sizes[::-1])",
        "options": [
            "[2, 7, 4, 9]",
            "[2, 4, 7, 9]",
            "[9, 4, 7, 2]",
            "[9, 7, 4, 2]",
        ],
        "correct": 2,
    },
    # ── 7. indexing is strict, slicing is forgiving ──
    {
        "question": "What happens when this runs?",
        "code_hint": "lst = [6, 1, 9]\nprint(lst[0:99])\nprint(lst[99])",
        "options": [
            "Both lines crash with IndexError",
            "[6, 1, 9]  then  9",
            "Both work: [6, 1, 9]  then  []",
            "[6, 1, 9]  then  IndexError",
        ],
        "correct": 3,
    },
    # ── 8. append returns None ──
    {
        "question": "What is printed?",
        "code_hint": "scores = [12, 5]\nscores = scores.append(30)\nprint(scores)",
        "options": [
            "[12, 5, 30]",
            "None",
            "[12, 5]",
            "Error — append takes no arguments",
        ],
        "correct": 1,
    },
    # ── 9. insert shifts everyone right ──
    {
        "question": "What is printed?",
        "code_hint": "pets = ['cat', 'dog', 'fish']\npets.insert(1, 'bird')\nprint(pets)",
        "options": [
            "['bird', 'cat', 'dog', 'fish']",
            "['cat', 'dog', 'bird', 'fish']",
            "['cat', 'bird', 'dog', 'fish']",
            "['cat', 'bird', 'fish']",
        ],
        "correct": 2,
    },
    # ── 10. pop hands the value back, del does not ──
    {
        "question": "What are the two printed values?",
        "code_hint": "temps = [19, 25, 31, 12]\nprint(temps.pop(1))\ndel temps[0]\nprint(temps)",
        "options": [
            "19  then  [25, 31, 12]",
            "25  then  [19, 31, 12]",
            "None  then  [31, 12]",
            "25  then  [31, 12]",
        ],
        "correct": 3,
    },
    # ── 11. the two ways to walk a list ──
    {
        "question": "What is the output of these two loops?",
        "code_hint": (
            "letters = ['a', 'b', 'c']\n"
            "for i in range(0, len(letters)):\n"
            '    print(i, end=" ")\n'
            "print()\n"
            "for letter in letters:\n"
            '    print(letter, end=" ")'
        ),
        "options": [
            "a b c\na b c",
            "0 1 2\n0 1 2",
            "1 2 3\na b c",
            "0 1 2\na b c",
        ],
        "correct": 3,
    },
    # ── 12. remove(x) deletes only the leftmost match ──
    {
        "question": "What is printed?",
        "code_hint": "nums = [4, 7, 4, 9, 4]\nnums.remove(4)\nprint(nums)",
        "options": [
            "[7, 9]",
            "[7, 4, 9, 4]",
            "[4, 7, 9, 4]",
            "[7, 4, 9]",
        ],
        "correct": 1,
    },
    # ── 13. remove on a value that is not there ──
    {
        "question": "What happens here?",
        "code_hint": "nums = [4, 7, 9]\nnums.remove(5)",
        "options": [
            "Nothing — 5 is simply ignored",
            "The list becomes [4, 7]",
            "ValueError — 5 is not in the list",
            "IndexError — there is no index 5",
        ],
        "correct": 2,
    },
    # ── 14. while x in lst: remove them all ──
    {
        "question": "What is printed?",
        "code_hint": "nums = [4, 7, 4, 9, 4]\nwhile 4 in nums:\n    nums.remove(4)\nprint(nums)",
        "options": [
            "[7, 4, 9, 4]",
            "[7, 9]",
            "[]",
            "Nothing — infinite loop",
        ],
        "correct": 1,
    },
    # ── 15. count(x) ──
    {
        "question": "What is printed?",
        "code_hint": "print([3, 6, 3, 3, 1].count(3))",
        "options": [
            "3",
            "2",
            "5",
            "0",
        ],
        "correct": 0,
    },
    # ── 16. in gives back a boolean ──
    {
        "question": "What are the two printed values?",
        "code_hint": "print(5 in [1, 2, 3])\nprint(2 in [1, 2, 3])",
        "options": [
            "True  then  True",
            "False  then  True",
            "Error — 'in' only works inside a for loop",
            "0  then  1",
        ],
        "correct": 1,
    },
    # ── 17. [x] * n builds a list ──
    {
        "question": "What is printed?",
        "code_hint": "row = [7] * 3\nrow.append(0)\nprint(row, len(row))",
        "options": [
            "[21, 0] 2",
            "[7, 3, 0] 3",
            "[7, 7, 7] 3",
            "[7, 7, 7, 0] 4",
        ],
        "correct": 3,
    },
    # ── 18. max, min, sum ──
    {
        "question": "What is printed?",
        "code_hint": "vals = [15, 4, 23, 8]\nprint(max(vals), min(vals), sum(vals))",
        "options": [
            "23 4 46",
            "15 4 50",
            "23 4 50",
            "4 23 50",
        ],
        "correct": 2,
    },
    # ── 19. the average is always a float ──
    {
        "question": "What is printed?",
        "code_hint": "grades = [10, 5, 6]\nprint(sum(grades) / len(grades))",
        "options": [
            "7",
            "7.0",
            "21",
            "There is no average — Python needs statistics.mean",
        ],
        "correct": 1,
    },
    # ── 20. building a list inside a loop ──
    {
        "question": "What is printed?",
        "code_hint": "squares = []\nfor i in range(1, 5):\n    squares.append(i * i)\nprint(squares)",
        "options": [
            "[1, 4, 9, 16, 25]",
            "[0, 1, 4, 9]",
            "[1, 4, 9, 16]",
            "[2, 4, 6, 8]",
        ],
        "correct": 2,
    },
]

QUESTIONS = ALL_QUESTIONS[:QUESTION_LIMIT]

TIME_LIMIT = 45


class Player:
    def __init__(self, ws: WebSocket, nickname: str, avatar: str):
        self.ws = ws
        self.nickname = nickname
        self.avatar = avatar
        self.score = 0
        self.connected = True


class GameManager:
    def __init__(self):
        self.host_ws: Optional[WebSocket] = None
        self.players: dict[str, Player] = {}
        self.state = "lobby"
        self.current_q_index = -1
        self.question_start_time: Optional[float] = None
        self.timer_task: Optional[asyncio.Task] = None
        self.answers_this_round: dict[str, dict] = {}
        self.reveal_triggered = False

    async def safe_send(self, ws: WebSocket, msg: dict):
        try:
            await ws.send_json(msg)
        except Exception:
            pass

    async def broadcast(self, msg: dict, include_host: bool = True):
        if include_host and self.host_ws:
            await self.safe_send(self.host_ws, msg)
        for player in list(self.players.values()):
            if player.connected and player.ws:
                await self.safe_send(player.ws, msg)

    async def send_host(self, msg: dict):
        if self.host_ws:
            await self.safe_send(self.host_ws, msg)

    def get_lobby_msg(self):
        return {
            "type": "lobby_update",
            "players": [
                {"nickname": n, "avatar": p.avatar}
                for n, p in self.players.items()
                if p.connected
            ],
        }

    def compute_scores(self):
        sorted_players = sorted(
            self.players.values(), key=lambda p: p.score, reverse=True
        )
        result = []
        rank = 1
        prev_score = None
        for i, p in enumerate(sorted_players):
            if prev_score is not None and p.score < prev_score:
                rank = i + 1
            result.append(
                {
                    "nickname": p.nickname,
                    "avatar": p.avatar,
                    "score": p.score,
                    "rank": rank,
                }
            )
            prev_score = p.score
        return result

    async def player_join(self, ws: WebSocket, nickname: str, avatar: str) -> bool:
        # Reconnect: player was in the game but lost connection
        if nickname in self.players and not self.players[nickname].connected:
            player = self.players[nickname]
            player.ws = ws
            player.connected = True
            await self.safe_send(ws, {"type": "joined", "nickname": nickname, "avatar": avatar})
            await self.send_current_state(ws, nickname)
            await self.send_host({"type": "player_rejoined", "nickname": nickname})
            return True

        if nickname in self.players:
            await self.safe_send(
                ws, {"type": "error", "message": "Nickname already taken!"}
            )
            return False
        if self.state != "lobby":
            await self.safe_send(
                ws, {"type": "error", "message": "Game already in progress!"}
            )
            return False
        self.players[nickname] = Player(ws, nickname, avatar)
        await self.broadcast(self.get_lobby_msg())
        await self.safe_send(ws, {"type": "joined", "nickname": nickname, "avatar": avatar})
        return True

    async def send_current_state(self, ws: WebSocket, nickname: str):
        """Replay the current game state to a reconnecting player."""
        player = self.players[nickname]
        if self.state == "lobby":
            await self.safe_send(ws, self.get_lobby_msg())

        elif self.state == "question":
            q = QUESTIONS[self.current_q_index]
            elapsed = time.time() - self.question_start_time
            remaining = max(0, int(TIME_LIMIT - elapsed))
            await self.safe_send(ws, {
                "type": "question",
                "index": self.current_q_index,
                "total": len(QUESTIONS),
                "question": q["question"],
                "options": q["options"],
                "time_limit": TIME_LIMIT,
                "code_hint": q["code_hint"],
            })
            await self.safe_send(ws, {"type": "timer", "remaining": remaining})
            if nickname in self.answers_this_round:
                await self.safe_send(ws, {
                    "type": "answer_received",
                    "answer_index": self.answers_this_round[nickname]["answer_index"],
                })

        elif self.state == "answer_reveal":
            q = QUESTIONS[self.current_q_index]
            correct = q["correct"]
            distribution = [0] * len(q["options"])
            for ans in self.answers_this_round.values():
                distribution[ans["answer_index"]] += 1
            ans_data = self.answers_this_round.get(nickname)
            points_earned = 0
            if ans_data and ans_data["answer_index"] == correct:
                ratio = max(0.0, 1.0 - ans_data["time_taken"] / TIME_LIMIT)
                points_earned = int(100 + 900 * ratio)
            await self.safe_send(ws, {
                "type": "answer_reveal",
                "correct_index": correct,
                "distribution": distribution,
                "options": q["options"],
                "your_answer": ans_data["answer_index"] if ans_data else None,
                "is_correct": bool(ans_data and ans_data["answer_index"] == correct),
                "points_earned": points_earned,
                "total_score": player.score,
            })

        elif self.state == "leaderboard":
            scores = self.compute_scores()
            is_last = self.current_q_index >= len(QUESTIONS) - 1
            await self.safe_send(ws, {
                "type": "leaderboard",
                "scores": scores,
                "is_last": is_last,
                "question_num": self.current_q_index + 1,
            })

        elif self.state == "game_over":
            scores = self.compute_scores()
            await self.safe_send(ws, {"type": "game_over", "scores": scores})

    async def player_disconnect(self, nickname: str):
        if nickname not in self.players:
            return
        if self.state == "lobby":
            # In lobby: fully remove them
            del self.players[nickname]
            await self.broadcast(self.get_lobby_msg())
        else:
            # Mid-game: keep their score, just mark offline
            self.players[nickname].connected = False
            self.players[nickname].ws = None
        await self.send_host(
            {
                "type": "player_left",
                "nickname": nickname,
                "total": len(self.players),
            }
        )

    async def start_game(self):
        if self.state != "lobby" or not self.players:
            return
        self.current_q_index = 0
        await self.show_question()

    async def show_question(self):
        self.state = "question"
        self.answers_this_round = {}
        self.reveal_triggered = False
        self.question_start_time = time.time()

        q = QUESTIONS[self.current_q_index]
        msg = {
            "type": "question",
            "index": self.current_q_index,
            "total": len(QUESTIONS),
            "question": q["question"],
            "options": q["options"],
            "time_limit": TIME_LIMIT,
            "code_hint": q["code_hint"],
        }
        await self.broadcast(msg)

        if self.timer_task and not self.timer_task.done():
            self.timer_task.cancel()
        self.timer_task = asyncio.create_task(self._run_timer())

    async def _run_timer(self):
        try:
            for remaining in range(TIME_LIMIT, -1, -1):
                await self.broadcast(
                    {"type": "timer", "remaining": remaining}, include_host=True
                )
                if remaining == 0:
                    break
                await asyncio.sleep(1)
            if self.state == "question" and not self.reveal_triggered:
                self.reveal_triggered = True
                await self.reveal_answers()
        except asyncio.CancelledError:
            pass

    async def receive_answer(self, nickname: str, answer_index: int):
        if self.state != "question":
            return
        if nickname not in self.players:
            return
        if nickname in self.answers_this_round:
            return

        time_taken = time.time() - self.question_start_time
        self.answers_this_round[nickname] = {
            "answer_index": answer_index,
            "time_taken": min(time_taken, TIME_LIMIT),
        }

        await self.safe_send(
            self.players[nickname].ws,
            {"type": "answer_received", "answer_index": answer_index},
        )
        await self.send_host(
            {
                "type": "player_answered",
                "nickname": nickname,
                "answered": len(self.answers_this_round),
                "total": len(self.players),
            }
        )

        connected_count = sum(1 for p in self.players.values() if p.connected)
        if (
            len(self.answers_this_round) >= connected_count
            and not self.reveal_triggered
        ):
            self.reveal_triggered = True
            asyncio.create_task(self._delayed_reveal())

    async def _delayed_reveal(self):
        await asyncio.sleep(1.5)
        if self.state == "question":
            if self.timer_task and not self.timer_task.done():
                self.timer_task.cancel()
            await self.reveal_answers()

    async def reveal_answers(self):
        if self.state != "question":
            return
        self.state = "answer_reveal"

        q = QUESTIONS[self.current_q_index]
        correct = q["correct"]

        distribution = [0] * len(q["options"])
        for ans in self.answers_this_round.values():
            distribution[ans["answer_index"]] += 1

        # Award points
        for nickname, ans_data in self.answers_this_round.items():
            if ans_data["answer_index"] == correct:
                ratio = max(0.0, 1.0 - ans_data["time_taken"] / TIME_LIMIT)
                points = int(100 + 900 * ratio)
                self.players[nickname].score += points

        # Personalized message per player
        for nickname, player in self.players.items():
            ans_data = self.answers_this_round.get(nickname)
            points_earned = 0
            if ans_data and ans_data["answer_index"] == correct:
                ratio = max(0.0, 1.0 - ans_data["time_taken"] / TIME_LIMIT)
                points_earned = int(100 + 900 * ratio)

            await self.safe_send(
                player.ws,
                {
                    "type": "answer_reveal",
                    "correct_index": correct,
                    "distribution": distribution,
                    "options": q["options"],
                    "your_answer": ans_data["answer_index"] if ans_data else None,
                    "is_correct": bool(
                        ans_data and ans_data["answer_index"] == correct
                    ),
                    "points_earned": points_earned,
                    "total_score": player.score,
                },
            )

        await self.send_host(
            {
                "type": "answer_reveal",
                "correct_index": correct,
                "distribution": distribution,
                "options": q["options"],
            }
        )

    async def show_leaderboard(self):
        if self.state != "answer_reveal":
            return
        self.state = "leaderboard"
        scores = self.compute_scores()
        is_last = self.current_q_index >= len(QUESTIONS) - 1
        await self.broadcast(
            {
                "type": "leaderboard",
                "scores": scores,
                "is_last": is_last,
                "question_num": self.current_q_index + 1,
            }
        )

    async def host_next(self):
        if self.state == "answer_reveal":
            await self.show_leaderboard()
        elif self.state == "leaderboard":
            if self.current_q_index < len(QUESTIONS) - 1:
                self.current_q_index += 1
                await self.show_question()
            else:
                await self.show_final()

    async def host_force_reveal(self):
        if self.state == "question" and not self.reveal_triggered:
            self.reveal_triggered = True
            if self.timer_task and not self.timer_task.done():
                self.timer_task.cancel()
            await self.reveal_answers()

    async def show_final(self):
        self.state = "game_over"
        scores = self.compute_scores()
        await self.broadcast({"type": "game_over", "scores": scores})

    async def restart(self):
        if self.timer_task and not self.timer_task.done():
            self.timer_task.cancel()
        # Keep only connected players, reset their scores
        self.players = {
            n: p for n, p in self.players.items() if p.connected
        }
        for player in self.players.values():
            player.score = 0
        self.state = "lobby"
        self.current_q_index = -1
        self.answers_this_round = {}
        self.reveal_triggered = False
        await self.broadcast(self.get_lobby_msg())


game = GameManager()


@app.get("/")
async def player_page():
    return FileResponse("static/index.html")


@app.get("/host")
async def host_page():
    return FileResponse("static/host.html")


@app.websocket("/ws/player")
async def player_websocket(websocket: WebSocket):
    await websocket.accept()
    nickname = None
    try:
        while True:
            data = await websocket.receive_json()
            t = data.get("type")
            if t == "join":
                ok = await game.player_join(
                    websocket, data["nickname"], data["avatar"]
                )
                if not ok:
                    break
                nickname = data["nickname"]
            elif t == "answer" and nickname:
                await game.receive_answer(nickname, data["answer_index"])
    except WebSocketDisconnect:
        pass
    finally:
        if nickname:
            await game.player_disconnect(nickname)


@app.websocket("/ws/host")
async def host_websocket(websocket: WebSocket):
    await websocket.accept()
    game.host_ws = websocket
    await websocket.send_json(game.get_lobby_msg())
    try:
        while True:
            data = await websocket.receive_json()
            t = data.get("type")
            if t == "start":
                await game.start_game()
            elif t == "next":
                await game.host_next()
            elif t == "force_reveal":
                await game.host_force_reveal()
            elif t == "restart":
                await game.restart()
    except WebSocketDisconnect:
        game.host_ws = None


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
