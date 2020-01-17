import pygame
import os.path
import random
import sys
pygame.init()  # Инициализация экрана pygame
screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()  # Создание таймера
FPS = 150


class Player(pygame.sprite.Sprite):  # Класс игрока
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group)
        self.radius = 10
        self.x = pos_x
        self.y = pos_y
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA, 32)  # Создание спрайта игрока
        pygame.draw.circle(self.image, pygame.Color("red"), (10, 10), self.radius)
        self.rect = pygame.Rect(self.x, self.y, 20, 20)
        self.mask = pygame.mask.from_surface(self.image)


class Tree(pygame.sprite.Sprite):  # Класс дерева
    def __init__(self, pos_x):
        super().__init__(all_sprites)
        self.radius = 10
        self.x = pos_x
        self.y = 500
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA, 32)  # Создание спрайта дерева
        pygame.draw.circle(self.image, (0, 100, 0), (10, 10), self.radius)
        self.rect = pygame.Rect(self.x, self.y, 20, 20)
        self.mask = pygame.mask.from_surface(self.image)


class Gates(pygame.sprite.Sprite):  # Создание класса ворот
    def __init__(self, pos_x):
        super().__init__(all_sprites)
        self.x = pos_x
        self.y = 500
        self.image = pygame.Surface((60, 10), pygame.SRCALPHA, 32)  # Создание спрайта ворот
        pygame.draw.circle(self.image, (0, 0, 100), (5, 5), 5)
        pygame.draw.circle(self.image, (0, 0, 100), (55, 5), 5)
        self.rect = pygame.Rect(self.x, self.y, 60, 10)
        self.mask = pygame.mask.from_surface(self.image)
        self.passed = False


class Particle(pygame.sprite.Sprite):  # Класс частицы (Для анимации салюта)
    fire = [(255, 0, 0), (0, 200, 0), (0, 0, 255),
            (0, 200, 200), (255, 0, 255), (200, 200, 0)]  # Возможные цвета частицы

    def __init__(self, pos, dx, dy):
        super().__init__(particles)
        self.image = pygame.Surface((4, 4), pygame.SRCALPHA, 32)  # Создание спрайта частицы
        pygame.draw.circle(self.image, random.choice(self.fire), (2, 2), 2)
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = 0.1

    def update(self):  # Анимация падения одной частицы
        self.velocity[1] += self.gravity
        self.rect.x += int(self.velocity[0])
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles(position):  # Салют: создание нескольких частиц в точке въезда в ворота
    particle_count = 30
    numbers = range(-6, 6)
    for _ in range(particle_count):
        Particle(position, float(random.choice(numbers)), float(random.choice(numbers)))


def load_image(name, color_key=None):  # Функция, отвечающая за загрузку картинки
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def start_screen():  # Функция, отвечающая за создание начальной заставки
    intro_text = ["Mountains skiing",
                  "",
                  "Правила игры:",
                  "Для смены направления движения",
                  "нажимайте стрелки влево и вправо.",
                  "Не врезайтесь в деревья.",
                  "Воротца принесут много очков.",
                  "Удачи! Для начала игры нажмите",
                  "любую клавишу."]  # Текст, который отображается в заставке
    fon = pygame.transform.scale(load_image('fon.png'), (500, 500))  # Создание фона заставки
    screen.blit(fon, (0, 0))
    background = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:  # Вывод текста на заставку
        string_rendered = background.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:  # Скрипт, отвецающий за контроль экрана заставки: выход при нажатии на крестик и переход к игре при
        # нажатии любой другой клавиши
        for j in pygame.event.get():
            if j.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif j.type == pygame.KEYDOWN or j.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


start_screen()  # Заставка
running = True  # Инициализаия необходимых для игры переменных, создание групп, создание игрока, чтение рекорда из файла
screen_rect = (0, 0, 500, 500)
a = 0
score = 0
player_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
particles = pygame.sprite.Group()
player = Player(250, 150)
player_group.add(player)
player_group.draw(screen)
alive = True
speed = 2
file = open('data/high_score.txt')
high_score = int(file.readline())
file.close()
scores = [high_score]
gates_passed = 0


def kill_player():  # Функция, отвечающая за окончание игры
    global alive, score, a, speed, gates_passed
    alive = False
    scores.append(score)
    score = 0
    a = 0
    speed = 2
    player.x = 250
    player.rect = pygame.Rect(250, 150, 20, 20)
    gates_passed = 0


while running:  # Главный цикл
    screen.fill((255, 255, 255))
    score += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Запись рекорда в файл при выходе из игры
            running = False
            os.remove('data/high_score.txt')
            f = open('data/high_score.txt', mode='w')
            f.write(str(max(scores)))
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:  # Движение влево
                if a == 0:
                    score = 0
                a = -1
                if alive is False:
                    player.x = 250
                    player.rect = pygame.Rect(250, 150, 20, 20)
                alive = True
            elif event.key == pygame.K_RIGHT:  # Движение вправо
                if a == 0:
                    score = 0
                a = 1
                if alive is False:
                    player.x = 250
                    player.rect = pygame.Rect(250, 150, 20, 20)
                alive = True
    if alive:  # Прорисовка всех спрайтов, вывод очков и рекорда
        particles.update()
        player_group.draw(screen)
        all_sprites.draw(screen)
        particles.draw(screen)
        font = pygame.font.Font(None, 25)
        text1 = font.render("Score: {}".format(score), 1, (0, 0, 0))
        text2 = font.render("High score: {}".format(max(scores)), 1, (0, 0, 0))
        text3 = font.render("Gates passed: {}".format(gates_passed), 1, (0, 0, 0))
        screen.blit(text1, (10, 10))
        screen.blit(text2, (10, 35))
        screen.blit(text3, (10, 60))
        pygame.display.flip()
        clock.tick(FPS)
        pygame.display.flip()        
        if score % 30 == 0:  # Создание новых деревьев/ворот
            x = random.random()
            if x >= 0.09:
                all_sprites.add(Tree(random.randrange(0, 480)))
            else:
                all_sprites.add(Gates(random.randrange(0, 440)))
        if score % 1000 == 0:  # Прибавление скорости
            speed += 1
        player.x += a  # Перемещение игрока
        player.rect = player.rect.move(a, 0)              
        for i in all_sprites:  # Перемещение препятствий вверх
            i.y -= speed
            i.rect = i.rect.move(0, speed * -1)
            if i.y < -10:  # Удаление препятствий, дошедших до верха
                i.kill()
            if str(type(i)) == "<class '__main__.Gates'>" and (i.y <= 150) and (i.y >= 140):
                if (player.x > i.x - 5) and (player.x < i.x + 55) and not i.passed:
                    new_score = score + (speed - 2) * 100  # Проход через ворота, добавление очков
                    if new_score // 1000 != score // 1000:
                        speed += 1
                    score = new_score
                    gates_passed += 1
                    create_particles((player.x, player.y))  # Салют
                    i.passed = True
            if pygame.sprite.collide_mask(player, i):  # Проверка на то, что игрок ни с кем не столкнулся
                kill_player()
            if alive is False:
                i.kill()    
        if player.x < -2 or player.x > 482:  # Проверка на то, что игрок не вышел за пределы экрана
            kill_player()
            for i in all_sprites:
                i.kill()
