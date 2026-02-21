<?php

declare(strict_types=1);

require_once __DIR__ . '/auth.php';

$user = requireUser();
$errors = [];
$success = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $projectName = trim($_POST['project_name'] ?? '');
    $eventDate = trim($_POST['event_date'] ?? '');
    $genre = trim($_POST['genre'] ?? '');
    $participation = trim($_POST['participation_format'] ?? '');

    if ($projectName === '') {
        $errors[] = 'Введите название музыкального проекта или мероприятия.';
    }

    if ($eventDate === '') {
        $errors[] = 'Выберите желаемую дату проведения.';
    }

    if ($genre === '') {
        $errors[] = 'Укажите жанр музыки.';
    }

    if ($participation === '') {
        $errors[] = 'Укажите формат участия.';
    }

    if (empty($errors)) {
        $stmt = db()->prepare('INSERT INTO requests (user_id, project_name, event_date, genre, participation_format, status, created_at)
            VALUES (:user_id, :project_name, :event_date, :genre, :participation, "Новая", :created_at)');
        $stmt->execute([
            'user_id' => $user['id'],
            'project_name' => $projectName,
            'event_date' => $eventDate,
            'genre' => $genre,
            'participation' => $participation,
            'created_at' => date('c'),
        ]);
        $success = 'Заявка отправлена и получила статус «Новая». ';
    }
}
?>
<!doctype html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GosdumaMusic — Новая заявка</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
<main class="container">
  <header class="nav">
    <h1>Новая музыкальная заявка</h1>
    <a class="btn btn-secondary" href="dashboard.php">Назад в кабинет</a>
  </header>
  <section class="card" style="max-width: 720px;">
    <?php foreach ($errors as $error): ?>
      <div class="message message-error" style="margin-bottom: 8px;"><?= htmlspecialchars($error) ?></div>
    <?php endforeach; ?>
    <?php if ($success): ?>
      <div class="message message-success"><?= htmlspecialchars($success) ?></div>
    <?php endif; ?>
    <form method="post" novalidate>
      <label>Название проекта/мероприятия
        <input type="text" name="project_name" required value="<?= htmlspecialchars($_POST['project_name'] ?? '') ?>">
      </label>
      <label>Желаемая дата проведения
        <input type="date" name="event_date" required value="<?= htmlspecialchars($_POST['event_date'] ?? '') ?>">
      </label>
      <label>Жанр музыки
        <input type="text" name="genre" required placeholder="Например, джаз" value="<?= htmlspecialchars($_POST['genre'] ?? '') ?>">
      </label>
      <label>Формат участия
        <select name="participation_format" required>
          <option value="">Выберите формат</option>
          <?php
          $options = ['Сольное выступление', 'Групповое выступление', 'Онлайн-участие'];
          $selected = $_POST['participation_format'] ?? '';
          foreach ($options as $option):
          ?>
            <option value="<?= htmlspecialchars($option) ?>" <?= $selected === $option ? 'selected' : '' ?>><?= htmlspecialchars($option) ?></option>
          <?php endforeach; ?>
        </select>
      </label>
      <button class="btn btn-primary" type="submit">Отправить</button>
    </form>
  </section>
</main>
</body>
</html>
