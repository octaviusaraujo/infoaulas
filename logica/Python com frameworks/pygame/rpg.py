"""RPG 16-bit em Pygame.

Controles:
- WASD ou setas: mover
- Espaco ou J: atacar
- E: abrir bau
- Tab: usar pocao
- Enter: iniciar / reiniciar
- Esc: sair
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from pathlib import Path

import pygame


WIDTH = 960
HEIGHT = 640
FPS = 60
TILE = 32
WORLD_W = 26
WORLD_H = 18
MAP_W = WORLD_W * TILE
MAP_H = WORLD_H * TILE

SKY = (167, 188, 214)
GRASS = (101, 139, 68)
GRASS_DARK = (74, 103, 52)
PATH = (167, 146, 108)
PANEL = (34, 28, 43)
PANEL_2 = (52, 44, 62)
TEXT = (244, 234, 198)
ACCENT = (255, 188, 69)
RED = (210, 70, 66)
WHITE = (248, 248, 248)
BLACK = (14, 14, 20)


ROOT = Path(__file__).resolve().parent
ASSET_DIR = ROOT / "imgs"


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def load_asset(name: str, size: tuple[int, int] | None = None, flip_x: bool = False) -> pygame.Surface | None:
    path = ASSET_DIR / name
    if not path.exists():
        return None
    try:
        image = pygame.image.load(str(path)).convert_alpha()
    except pygame.error:
        return None
    bbox = image.get_bounding_rect()
    if bbox.width > 0 and bbox.height > 0:
        image = image.subsurface(bbox).copy()
    if flip_x:
        image = pygame.transform.flip(image, True, False)
    if size is not None:
        image = pygame.transform.smoothscale(image, size)
    return image


def make_shadow(size: tuple[int, int]) -> pygame.Surface:
    surf = pygame.Surface(size, pygame.SRCALPHA)
    pygame.draw.ellipse(surf, (0, 0, 0, 90), surf.get_rect())
    return surf


def draw_pixel_rect(surface: pygame.Surface, rect: pygame.Rect, color: tuple[int, int, int], border: int = 0) -> None:
    pygame.draw.rect(surface, color, rect)
    if border:
        pygame.draw.rect(surface, BLACK, rect, border)


def bob_frame(image: pygame.Surface, dy: int = 0) -> pygame.Surface:
    surf = pygame.Surface(image.get_size(), pygame.SRCALPHA)
    surf.blit(image, (0, dy))
    return surf


def build_hero_frames() -> dict[str, list[pygame.Surface]]:
    front = load_asset("front.png", (56, 56))
    back = load_asset("back.png", (56, 56))
    side = load_asset("side.png", (56, 56))
    if front is not None and back is not None and side is not None:
        side_left = pygame.transform.flip(side, True, False)
        return {
            "down": [front, bob_frame(front, 1)],
            "up": [back, bob_frame(back, 1)],
            "side_right": [side, bob_frame(side, 1)],
            "side_left": [side_left, bob_frame(side_left, 1)],
        }
    return build_hero_frames_fallback()


def build_hero_frames_fallback() -> dict[str, list[pygame.Surface]]:
    frames: dict[str, list[pygame.Surface]] = {
        "down": [make_hero_frame("down", 0), make_hero_frame("down", 1)],
        "up": [make_hero_frame("up", 0), make_hero_frame("up", 1)],
        "side_right": [make_hero_frame("side", 0), make_hero_frame("side", 1)],
        "side_left": [
            pygame.transform.flip(make_hero_frame("side", 0), True, False),
            pygame.transform.flip(make_hero_frame("side", 1), True, False),
        ],
    }
    return frames


def make_hero_frame(direction: str, step: int) -> pygame.Surface:
    surf = pygame.Surface((56, 56), pygame.SRCALPHA)
    bob = 1 if step == 1 else 0
    cloak = (128, 72, 45)
    cloth = (172, 138, 108)
    skin = (244, 190, 142)
    hair = (102, 58, 47)
    outline = BLACK
    pygame.draw.ellipse(surf, hair, pygame.Rect(12, 4 + bob, 32, 26))
    pygame.draw.ellipse(surf, outline, pygame.Rect(12, 4 + bob, 32, 26), 2)
    pygame.draw.rect(surf, skin, pygame.Rect(20, 16 + bob, 16, 12))
    pygame.draw.rect(surf, outline, pygame.Rect(20, 16 + bob, 16, 12), 1)
    pygame.draw.polygon(surf, cloak, [(12, 24 + bob), (44, 24 + bob), (38, 48 + bob), (18, 48 + bob)])
    pygame.draw.polygon(surf, outline, [(12, 24 + bob), (44, 24 + bob), (38, 48 + bob), (18, 48 + bob)], 2)
    pygame.draw.rect(surf, cloth, pygame.Rect(19, 26 + bob, 18, 12))
    pygame.draw.rect(surf, outline, pygame.Rect(19, 26 + bob, 18, 12), 1)
    pygame.draw.rect(surf, (74, 54, 50), pygame.Rect(18, 44 + bob, 8, 10))
    pygame.draw.rect(surf, (74, 54, 50), pygame.Rect(30, 44 + bob, 8, 10))
    pygame.draw.rect(surf, outline, pygame.Rect(18, 44 + bob, 8, 10), 1)
    pygame.draw.rect(surf, outline, pygame.Rect(30, 44 + bob, 8, 10), 1)
    if direction == "side":
        pygame.draw.rect(surf, cloth, pygame.Rect(10, 24 + bob, 8, 14))
        pygame.draw.rect(surf, cloth, pygame.Rect(38, 24 + bob, 8, 14))
        sword_x = 41 if step == 0 else 42
        pygame.draw.line(surf, (226, 214, 187), (sword_x, 36 + bob), (54, 40 + bob), 4)
        pygame.draw.line(surf, (97, 69, 46), (38, 38 + bob), (54, 42 + bob), 2)
    else:
        pygame.draw.rect(surf, cloth, pygame.Rect(8, 24 + bob, 8, 14))
        pygame.draw.rect(surf, cloth, pygame.Rect(40, 24 + bob, 8, 14))
        pygame.draw.line(surf, (226, 214, 187), (4, 40 + bob), (14, 38 + bob), 4)
        pygame.draw.line(surf, (97, 69, 46), (42, 38 + bob), (52, 42 + bob), 4)
    return surf


def build_slime_frames() -> list[pygame.Surface]:
    slime = load_asset("slime.png", (44, 34))
    if slime is not None:
        return [slime, bob_frame(slime, 1)]
    frames = []
    for step in (0, 1):
        surf = pygame.Surface((44, 34), pygame.SRCALPHA)
        bob = 2 if step else 0
        pygame.draw.ellipse(surf, (76, 160, 220), pygame.Rect(4, 5 + bob, 36, 24))
        pygame.draw.ellipse(surf, (32, 82, 122), pygame.Rect(4, 5 + bob, 36, 24), 2)
        pygame.draw.arc(surf, (30, 58, 84), pygame.Rect(12, 12 + bob, 20, 10), math.pi, 2 * math.pi, 2)
        pygame.draw.circle(surf, WHITE, (15, 15 + bob), 2)
        pygame.draw.circle(surf, WHITE, (28, 14 + bob), 2)
        frames.append(surf)
    return frames


def build_chest() -> pygame.Surface:
    chest = load_asset("bau.png", (44, 34))
    if chest is not None:
        return chest
    surf = pygame.Surface((44, 34), pygame.SRCALPHA)
    pygame.draw.rect(surf, (120, 76, 48), pygame.Rect(4, 10, 36, 18))
    pygame.draw.rect(surf, (184, 132, 92), pygame.Rect(4, 10, 36, 18), 2)
    pygame.draw.rect(surf, (98, 61, 35), pygame.Rect(18, 6, 8, 22))
    pygame.draw.rect(surf, (42, 30, 28), pygame.Rect(19, 19, 6, 6))
    pygame.draw.rect(surf, (225, 182, 104), pygame.Rect(7, 13, 30, 4))
    return surf


def build_coin() -> pygame.Surface:
    coin = load_asset("moeda.png", (26, 26))
    if coin is not None:
        return coin
    surf = pygame.Surface((26, 26), pygame.SRCALPHA)
    pygame.draw.circle(surf, (255, 205, 68), (13, 13), 11)
    pygame.draw.circle(surf, (143, 104, 20), (13, 13), 11, 2)
    pygame.draw.line(surf, (255, 233, 150), (10, 5), (17, 21), 3)
    return surf


def build_potion() -> pygame.Surface:
    potion = load_asset("pocao.png", (26, 34))
    if potion is not None:
        return potion
    surf = pygame.Surface((26, 34), pygame.SRCALPHA)
    pygame.draw.rect(surf, (215, 222, 234), pygame.Rect(9, 5, 8, 7))
    pygame.draw.rect(surf, (156, 164, 179), pygame.Rect(9, 5, 8, 7), 1)
    pygame.draw.ellipse(surf, (214, 56, 58), pygame.Rect(4, 12, 18, 17))
    pygame.draw.ellipse(surf, (110, 20, 28), pygame.Rect(4, 12, 18, 17), 2)
    pygame.draw.rect(surf, (173, 122, 82), pygame.Rect(11, 2, 4, 8))
    return surf


def build_tiles() -> tuple[pygame.Surface, pygame.Surface]:
    stone = load_asset("Fundo.png", (TILE, TILE))
    grass = load_asset("grama.png", (TILE, TILE))
    if stone is not None and grass is not None:
        return stone, grass
    stone = pygame.Surface((TILE, TILE))
    stone.fill((131, 120, 136))
    pygame.draw.rect(stone, (94, 83, 104), stone.get_rect(), 2)
    for _ in range(3):
        pygame.draw.line(stone, (111, 102, 119), (random.randint(2, 28), random.randint(2, 28)), (random.randint(2, 28), random.randint(2, 28)), 1)
    grass = pygame.Surface((TILE, TILE))
    grass.fill(GRASS)
    pygame.draw.rect(grass, GRASS_DARK, grass.get_rect(), 2)
    for _ in range(5):
        pygame.draw.line(grass, (132, 170, 88), (random.randint(0, 31), random.randint(0, 31)), (random.randint(0, 31), random.randint(0, 31)), 1)
    return stone, grass


def build_sword_icon() -> pygame.Surface:
    sword = load_asset("espada.png", (34, 34))
    if sword is not None:
        return sword
    surf = pygame.Surface((34, 34), pygame.SRCALPHA)
    pygame.draw.line(surf, (237, 215, 182), (6, 26), (26, 6), 5)
    pygame.draw.line(surf, (114, 78, 46), (5, 27), (27, 5), 2)
    pygame.draw.line(surf, (131, 87, 52), (6, 27), (15, 18), 4)
    pygame.draw.line(surf, (82, 47, 39), (2, 30), (12, 20), 4)
    return surf


@dataclass
class Chest:
    rect: pygame.Rect
    opened: bool = False
    gold: int = 0
    potion: int = 0


class Enemy:
    def __init__(self, x: int, y: int, frames: list[pygame.Surface]):
        self.rect = pygame.Rect(x, y, 30, 24)
        self.frames = frames
        self.frame = 0
        self.anim = 0.0
        self.speed = random.choice([0.7, 0.8, 0.9, 1.0])
        self.hp = 2
        self.dead = False
        self.hit_flash = 0.0

    def update(self, player: "Player", dt: float) -> None:
        if self.dead:
            return
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        dist = max(1.0, math.hypot(dx, dy))
        if dist < 220:
            self.rect.x += int(round((dx / dist) * self.speed * 90 * dt))
            self.rect.y += int(round((dy / dist) * self.speed * 90 * dt))
        self.rect.x = int(clamp(self.rect.x, 0, MAP_W - self.rect.width))
        self.rect.y = int(clamp(self.rect.y, 0, MAP_H - self.rect.height))
        self.anim += dt
        if self.anim >= 0.28:
            self.anim = 0.0
            self.frame = (self.frame + 1) % len(self.frames)
        if self.hit_flash > 0:
            self.hit_flash -= dt

    def draw(self, surface: pygame.Surface, camera: pygame.Vector2) -> None:
        if self.dead:
            return
        img = self.frames[self.frame]
        camx = int(camera.x)
        camy = int(camera.y)
        pos = (self.rect.x - camx - 6, self.rect.y - camy - 8)
        surface.blit(img, pos)
        if self.hit_flash > 0:
            overlay = pygame.Surface(img.get_size(), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 80))
            surface.blit(overlay, pos)


class Player:
    def __init__(self, x: int, y: int, frames: dict[str, list[pygame.Surface]], sword_icon: pygame.Surface):
        self.rect = pygame.Rect(x, y, 28, 28)
        self.frames = frames
        self.facing = "down"
        self.frame = 0
        self.anim = 0.0
        self.speed = 160
        self.hp = 10
        self.hp_max = 10
        self.gold = 0
        self.potions = 1
        self.attack_timer = 0.0
        self.attack_cooldown = 0.0
        self.invuln = 0.0
        self.sword_icon = sword_icon
        self.last_move = pygame.Vector2(0, 1)

    def update(self, dt: float, keys: pygame.key.ScancodeWrapper, world: "World") -> None:
        move = pygame.Vector2(0, 0)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move.x -= 1
            self.facing = "side_left"
            self.last_move = pygame.Vector2(-1, 0)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move.x += 1
            self.facing = "side_right"
            self.last_move = pygame.Vector2(1, 0)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            move.y -= 1
            self.facing = "up"
            self.last_move = pygame.Vector2(0, -1)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            move.y += 1
            self.facing = "down"
            self.last_move = pygame.Vector2(0, 1)
        if move.length_squared() > 0:
            move = move.normalize() * self.speed * dt
            self.move_axis(move.x, 0, world)
            self.move_axis(0, move.y, world)
            self.anim += dt
            if self.anim >= 0.16:
                self.anim = 0.0
                self.frame = (self.frame + 1) % len(self.frames[self.facing])
        else:
            self.frame = 0
        if self.attack_timer > 0:
            self.attack_timer -= dt
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt
        if self.invuln > 0:
            self.invuln -= dt

    def move_axis(self, dx: float, dy: float, world: "World") -> None:
        self.rect.x += int(round(dx))
        self.rect.y += int(round(dy))
        self.rect.x = int(clamp(self.rect.x, 0, MAP_W - self.rect.width))
        self.rect.y = int(clamp(self.rect.y, 0, MAP_H - self.rect.height))
        for wall in world.walls:
            if self.rect.colliderect(wall):
                if dx > 0:
                    self.rect.right = wall.left
                elif dx < 0:
                    self.rect.left = wall.right
                if dy > 0:
                    self.rect.bottom = wall.top
                elif dy < 0:
                    self.rect.top = wall.bottom

    def attack(self, world: "World") -> None:
        if self.attack_cooldown > 0:
            return
        self.attack_timer = 0.16
        self.attack_cooldown = 0.28
        reach = pygame.Rect(self.rect)
        if self.facing == "up":
            reach.inflate_ip(-6, -6)
            reach.y -= 26
        elif self.facing == "down":
            reach.inflate_ip(-6, -6)
            reach.y += 18
        else:
            if self.last_move.x < 0:
                reach.x -= 24
            else:
                reach.x += 24
            reach.inflate_ip(-2, -6)
        for enemy in world.enemies:
            if not enemy.dead and reach.colliderect(enemy.rect):
                enemy.hp -= 1
                enemy.hit_flash = 0.12
                if enemy.hp <= 0:
                    enemy.dead = True
                    self.gold += random.randint(1, 3)

    def draw(self, surface: pygame.Surface, camera: pygame.Vector2) -> None:
        img = self.frames[self.facing][self.frame]
        camx = int(camera.x)
        camy = int(camera.y)
        pos = (self.rect.x - camx - 14, self.rect.y - camy - 18)
        shadow = make_shadow((34, 10))
        surface.blit(shadow, (self.rect.x - camx - 3, self.rect.y - camy + 20))
        surface.blit(img, pos)
        if self.attack_timer > 0:
            if self.facing == "up":
                sword = pygame.Rect(self.rect.centerx - 2 - camx, self.rect.top - 18 - camy, 10, 20)
            elif self.facing == "down":
                sword = pygame.Rect(self.rect.centerx - 2 - camx, self.rect.bottom - 6 - camy, 10, 20)
            elif self.last_move.x < 0:
                sword = pygame.Rect(self.rect.left - 20 - camx, self.rect.centery - 6 - camy, 20, 10)
            else:
                sword = pygame.Rect(self.rect.right - 2 - camx, self.rect.centery - 6 - camy, 20, 10)
            pygame.draw.rect(surface, (238, 218, 190), sword)
            pygame.draw.rect(surface, (110, 80, 52), sword, 2)


class World:
    def __init__(self):
        self.tile_stone, self.tile_grass = build_tiles()
        self.chest_sprite = build_chest()
        self.coin_sprite = build_coin()
        self.potion_sprite = build_potion()
        self.sword_icon = build_sword_icon()
        self.hero_frames = build_hero_frames()
        self.slime_frames = build_slime_frames()
        self.title_art = load_asset("Fundo.png", (280, 280))
        self.walls: list[pygame.Rect] = []
        self.chests: list[Chest] = []
        self.enemies: list[Enemy] = []
        self._build_map()
        self.player = Player(4 * TILE, 4 * TILE, self.hero_frames, self.sword_icon)
        self.time = 0.0
        self.state = "title"
        self.message = "Pressione Enter para jogar"
        self.message_timer = 0.0
        self.spawn_timer = 0.0
        self.quest_gold = 18
        self.quest_text = "Colete 18 moedas para vencer"

    def _build_map(self) -> None:
        rng = random.Random(16)
        for y in range(WORLD_H):
            for x in range(WORLD_W):
                if x in (0, WORLD_W - 1) or y in (0, WORLD_H - 1):
                    self.walls.append(pygame.Rect(x * TILE, y * TILE, TILE, TILE))
                elif (x in (8, 9, 10, 17, 18) and 4 <= y <= 5) or (y in (11, 12) and 5 <= x <= 8):
                    if rng.random() < 0.7:
                        self.walls.append(pygame.Rect(x * TILE, y * TILE, TILE, TILE))

        chest_points = [(6, 6), (20, 6), (11, 13)]
        for cx, cy in chest_points:
            self.chests.append(Chest(pygame.Rect(cx * TILE + 2, cy * TILE + 6, 24, 18), gold=random.randint(6, 12), potion=random.choice([0, 1])))

        for px, py in [(5, 4), (12, 4), (20, 9), (8, 12), (18, 13)]:
            self.enemies.append(Enemy(px * TILE, py * TILE, self.slime_frames))

    def update(self, dt: float, keys: pygame.key.ScancodeWrapper) -> None:
        self.time += dt
        if self.state != "playing":
            return
        self.player.update(dt, keys, self)
        if self.player.attack_cooldown <= 0 and (keys[pygame.K_SPACE] or keys[pygame.K_j]):
            self.player.attack(self)

        for enemy in self.enemies:
            enemy.update(self.player, dt)
            if not enemy.dead and enemy.rect.colliderect(self.player.rect) and self.player.invuln <= 0:
                self.player.hp -= 1
                self.player.invuln = 0.8
                self.message = "O slime acertou voce!"
                self.message_timer = 1.3

        self.enemies = [enemy for enemy in self.enemies if not enemy.dead]

        self.spawn_timer -= dt
        if self.spawn_timer <= 0 and len(self.enemies) < 7:
            self.spawn_timer = 4.5
            self.spawn_enemy()

        if keys[pygame.K_e]:
            self.try_open_chest()

        if self.player.gold >= self.quest_gold:
            self.state = "victory"
            self.message = "Voce venceu! Pressione Enter para jogar de novo."
        if self.player.hp <= 0:
            self.state = "gameover"
            self.message = "Game Over. Pressione Enter para tentar de novo."

        if self.message_timer > 0:
            self.message_timer -= dt
            if self.message_timer <= 0 and self.state == "playing":
                self.message = self.quest_text

    def spawn_enemy(self) -> None:
        spots = [(3, 3), (22, 3), (4, 14), (21, 13), (14, 8)]
        random.shuffle(spots)
        for sx, sy in spots:
            rect = pygame.Rect(sx * TILE, sy * TILE, 30, 24)
            if not any(rect.colliderect(w) for w in self.walls):
                self.enemies.append(Enemy(rect.x, rect.y, self.slime_frames))
                return

    def try_open_chest(self) -> None:
        for chest in self.chests:
            if not chest.opened and self.player.rect.colliderect(chest.rect.inflate(12, 12)):
                chest.opened = True
                self.player.gold += chest.gold
                self.player.potions += chest.potion
                self.message = f"Bau aberto: +{chest.gold} ouro"
                if chest.potion:
                    self.message += " e +1 pocao"
                self.message_timer = 1.5
                break

    def use_potion(self) -> None:
        if self.player.potions <= 0 or self.player.hp >= self.player.hp_max:
            return
        self.player.potions -= 1
        self.player.hp = min(self.player.hp_max, self.player.hp + 3)
        self.message = "Voce usou uma pocao."
        self.message_timer = 1.1

    def restart(self) -> None:
        self.__init__()
        self.state = "playing"
        self.message = self.quest_text

    def draw_background(self, screen: pygame.Surface) -> None:
        screen.fill(SKY)
        for y in range(WORLD_H):
            for x in range(WORLD_W):
                rect = pygame.Rect(x * TILE, y * TILE, TILE, TILE)
                if x in (0, WORLD_W - 1) or y in (0, WORLD_H - 1):
                    screen.blit(self.tile_stone, rect)
                else:
                    screen.blit(self.tile_grass, rect)
        for px, py, pw, ph in [
            (7, 3, 12, 1),
            (12, 7, 1, 6),
            (3, 10, 7, 1),
            (15, 4, 5, 1),
        ]:
            pygame.draw.rect(screen, PATH, pygame.Rect(px * TILE, py * TILE, pw * TILE, ph * TILE))
        for px, py in [(9, 8), (10, 8), (16, 12), (19, 7), (4, 13), (22, 11)]:
            pygame.draw.circle(screen, (92, 151, 73), (px * TILE + 14, py * TILE + 16), 6)

    def draw_ui(self, screen: pygame.Surface, font: pygame.font.Font, small: pygame.font.Font) -> None:
        ui = pygame.Rect(18, 18, 280, 120)
        draw_pixel_rect(screen, ui, PANEL, 3)
        pygame.draw.rect(screen, PANEL_2, ui.inflate(-8, -8))
        title = font.render("Aldeia dos Ecos", True, TEXT)
        screen.blit(title, (30, 28))

        hp_label = small.render(f"HP {self.player.hp}/{self.player.hp_max}", True, TEXT)
        gold_label = small.render(f"Ouro {self.player.gold}", True, TEXT)
        potion_label = small.render(f"Pocoes {self.player.potions}", True, TEXT)
        quest_label = small.render(self.quest_text, True, ACCENT)
        screen.blit(hp_label, (30, 58))
        screen.blit(gold_label, (30, 82))
        screen.blit(potion_label, (30, 102))
        screen.blit(quest_label, (30, 124))

        for i in range(self.player.hp_max):
            color = RED if i < self.player.hp else (84, 70, 79)
            pygame.draw.rect(screen, color, pygame.Rect(180 + i * 12, 60, 10, 10))
            pygame.draw.rect(screen, BLACK, pygame.Rect(180 + i * 12, 60, 10, 10), 1)

        if self.message:
            banner = pygame.Rect(18, HEIGHT - 74, WIDTH - 36, 44)
            draw_pixel_rect(screen, banner, PANEL, 3)
            pygame.draw.rect(screen, PANEL_2, banner.inflate(-8, -8))
            msg = small.render(self.message, True, TEXT)
            screen.blit(msg, (32, HEIGHT - 56))

        inv = pygame.Rect(WIDTH - 146, 18, 128, 64)
        draw_pixel_rect(screen, inv, PANEL, 3)
        pygame.draw.rect(screen, PANEL_2, inv.inflate(-8, -8))
        screen.blit(self.sword_icon, (WIDTH - 128, 28))
        screen.blit(small.render("Ataque", True, TEXT), (WIDTH - 82, 30))
        screen.blit(self.coin_sprite, (WIDTH - 132, 54))
        screen.blit(small.render("Baus", True, TEXT), (WIDTH - 82, 58))

    def draw(self, screen: pygame.Surface, font: pygame.font.Font, small: pygame.font.Font) -> None:
        self.draw_background(screen)
        camera = pygame.Vector2(
            clamp(self.player.rect.centerx - WIDTH / 2, 0, MAP_W - WIDTH),
            clamp(self.player.rect.centery - HEIGHT / 2, 0, MAP_H - HEIGHT),
        )
        camx = int(camera.x)
        camy = int(camera.y)
        for chest in self.chests:
            sprite = self.chest_sprite.copy()
            if chest.opened:
                sprite.fill((120, 88, 62), special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(sprite, (chest.rect.x - camx - 6, chest.rect.y - camy - 8))
        for enemy in self.enemies:
            enemy.draw(screen, camera)
        self.player.draw(screen, camera)
        self.draw_ui(screen, font, small)

        if self.state == "title":
            self.draw_title(screen, font, small)
        elif self.state in ("victory", "gameover"):
            self.draw_end(screen, font, small)

    def draw_title(self, screen: pygame.Surface, font: pygame.font.Font, small: pygame.font.Font) -> None:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((11, 15, 28, 160))
        screen.blit(overlay, (0, 0))
        panel = pygame.Rect(190, 120, 580, 380)
        draw_pixel_rect(screen, panel, PANEL, 4)
        pygame.draw.rect(screen, PANEL_2, panel.inflate(-8, -8))
        title = font.render("RPG 16-BIT", True, TEXT)
        subtitle = small.render("Exploracao, combate e baus em um mapa pixelado", True, ACCENT)
        hint1 = small.render("Enter: iniciar", True, TEXT)
        hint2 = small.render("WASD/Setas: mover | Espaco: atacar | E: abrir baus", True, TEXT)
        screen.blit(title, (panel.centerx - title.get_width() // 2, 170))
        screen.blit(subtitle, (panel.centerx - subtitle.get_width() // 2, 232))
        if self.title_art is not None:
            screen.blit(self.title_art, (panel.centerx - self.title_art.get_width() // 2, 250))
        screen.blit(self.hero_frames["down"][0], (panel.centerx - 28, 292))
        screen.blit(hint1, (panel.centerx - hint1.get_width() // 2, 340))
        screen.blit(hint2, (panel.centerx - hint2.get_width() // 2, 370))

    def draw_end(self, screen: pygame.Surface, font: pygame.font.Font, small: pygame.font.Font) -> None:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((8, 11, 18, 170))
        screen.blit(overlay, (0, 0))
        panel = pygame.Rect(220, 180, 520, 220)
        draw_pixel_rect(screen, panel, PANEL, 4)
        pygame.draw.rect(screen, PANEL_2, panel.inflate(-8, -8))
        label = font.render("VITORIA" if self.state == "victory" else "FIM DE JOGO", True, TEXT)
        hint = small.render("Enter: reiniciar", True, ACCENT)
        screen.blit(label, (panel.centerx - label.get_width() // 2, 230))
        screen.blit(hint, (panel.centerx - hint.get_width() // 2, 300))


def main() -> None:
    pygame.init()
    pygame.display.set_caption("RPG 16-bit")
    pygame.key.set_repeat(150, 40)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 42)
    small = pygame.font.Font(None, 28)
    world = World()

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_RETURN:
                    if world.state == "title":
                        world.state = "playing"
                        world.message = world.quest_text
                    else:
                        world.restart()
                elif event.key == pygame.K_TAB and world.state == "playing":
                    world.use_potion()

        keys = pygame.key.get_pressed()
        if world.state == "playing":
            world.update(dt, keys)
        elif world.state == "title":
            if keys[pygame.K_RETURN]:
                world.state = "playing"
                world.message = world.quest_text
        elif world.state in ("victory", "gameover"):
            if keys[pygame.K_RETURN]:
                world.restart()

        world.draw(screen, font, small)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
