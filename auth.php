<?php

declare(strict_types=1);

require_once __DIR__ . '/db.php';

if (session_status() !== PHP_SESSION_ACTIVE) {
    session_start();
}

function currentUser(): ?array
{
    if (!isset($_SESSION['user_id'])) {
        return null;
    }

    $stmt = db()->prepare('SELECT * FROM users WHERE id = :id');
    $stmt->execute(['id' => $_SESSION['user_id']]);
    $user = $stmt->fetch();

    return $user ?: null;
}

function requireUser(): array
{
    $user = currentUser();

    if ($user === null) {
        header('Location: index.php');
        exit;
    }

    return $user;
}

function requireAdmin(): void
{
    if (empty($_SESSION['is_admin'])) {
        header('Location: index.php');
        exit;
    }
}
