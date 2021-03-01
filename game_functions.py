import pygame
import sys
from alien import Alien

from bullet import Bullet

from time import sleep


def fire_bullet(settings, screen, ship, bullets):
    if len(bullets) < settings.bullet_allowed:
        new_bullet = Bullet(settings, screen, ship)
        bullets.add(new_bullet)


def check_events(settings, screen, ship, bullets, stats, play_button, scoreboard):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                ship.moving_right = True
            elif event.key == pygame.K_LEFT:
                ship.moving_left = True
            elif event.key == pygame.K_SPACE:
                fire_bullet(settings, screen, ship, bullets)
            elif event.key == pygame.K_q:
                sys.exit()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                ship.moving_right = False
            elif event.key == pygame.K_LEFT:
                ship.moving_left = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(settings, stats, play_button, mouse_x, mouse_y, scoreboard)


def update_bullets(settings, screen, ship, bullets, aliens, stats, scoreboard):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <=0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(settings, screen, ship, bullets, aliens, stats, scoreboard)


def update_screen(settings, screen, ship, bullets, aliens, stats, play_button, scoreboard):
    screen.fill(settings.bg_color)
    ship.blitme()
    for bullet in bullets:
        bullet.draw()
    aliens.draw(screen)

    scoreboard.show_score()

    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()


def update_aliens(settings, screen, ship, bullets, aliens, stats, scoreboard):
    check_fleet_edges(settings, aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(settings, screen, ship, bullets, aliens, stats, scoreboard)

    check_aliens_bottom(settings, screen, ship, bullets, aliens, stats, scoreboard)


def change_fleet_direction(settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += settings.fleet_drop_speed
    settings.fleet_direction *= -1


def check_fleet_edges(settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(settings, aliens)
            break


def get_number_aliens_x(settings, alien_width):
    available_space_x = settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(settings, ship_height, alien_height):
    available_space_y = (settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(settings, screen, aliens, alien_number, row_number):
    alien = Alien(settings, screen)
    alien_width = alien.rect.width

    alien = Alien(settings, screen)
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(settings, screen, ship, aliens):
    alien = Alien(settings, screen)
    number_aliens_x = get_number_aliens_x(settings, alien.rect.width)
    number_rows = get_number_rows(settings, ship.rect.height, alien.rect.height)

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(settings, screen, aliens, alien_number, row_number)


def ship_hit(settings, screen, ship, bullets, aliens, stats, scoreboard):
    if stats.ships_left > 0:
        stats.ships_left -= 1
        scoreboard.prep_ships()

        aliens.empty()
        bullets.empty()

        create_fleet(settings, screen, ship, aliens)
        ship.center_ship()

        sleep(1)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(settings, screen, ship, bullets, aliens, stats, scoreboard):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(settings, screen, ship, bullets, aliens, stats, scoreboard)
            break


def check_play_button(settings, stats, play_button, mouse_x, mouse_y, scoreboard):
    if play_button.rect.collidepoint(mouse_x, mouse_y) and not stats.game_active:
        settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True

        scoreboard.prep_high_score()
        scoreboard.prep_score()
        scoreboard.prep_level()
        scoreboard.prep_ships()


def check_bullet_alien_collisions(settings, screen, ship, bullets, aliens, stats, scoreboard):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += settings.alien_points * len(aliens)
        scoreboard.prep_score()
        check_high_score(stats, scoreboard)

    if len(aliens) == 0:
        settings.increase_speed()
        stats.level +=1
        scoreboard.prep_level()
        bullets.empty()
        create_fleet(settings, screen, ship, aliens)


def check_high_score(stats, scoreboard):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        scoreboard.prep_high_score()
