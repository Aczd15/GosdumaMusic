<?php

declare(strict_types=1);

require_once __DIR__ . '/auth.php';

$user = requireUser();

$stmt = db()->prepare('SELECT * FROM requests WHERE user_id = :user_id ORDER BY id DESC');
$stmt->execute(['user_id' => $user['id']]);
$requests = $stmt->fetchAll();

function statusClass(string $status): string
{
    return match ($status) {
        'На рассмотрении' => 'status-review',
        'Одобрена' => 'status-approved',
        'Отклонена' => 'status-rejected',
        default => 'status-new',
    };
}
?>
<!doctype html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GosdumaMusic — Личный кабинет</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
<main class="container">
  <header class="nav">
    <h1>Личный кабинет</h1>
    <div class="nav-links">
      <a class="btn btn-secondary" href="create_request.php">Новая заявка</a>
      <a class="btn btn-primary" href="logout.php">Выйти</a>
    </div>
  </header>

  <section class="card">
    <h2>Профиль</h2>
    <div class="grid-two">
      <p><strong>Логин:</strong> <?= htmlspecialchars($user['login']) ?></p>
      <p><strong>ФИО:</strong> <?= htmlspecialchars($user['full_name']) ?></p>
      <p><strong>Телефон:</strong> <?= htmlspecialchars($user['phone']) ?></p>
      <p><strong>E-mail:</strong> <?= htmlspecialchars($user['email']) ?></p>
    </div>
  </section>

  <section class="card" style="margin-top: 16px;">
    <h2>Мои музыкальные заявки</h2>
    <?php if (empty($requests)): ?>
      <div class="message message-success">У вас пока нет созданных заявок. Нажмите «Новая заявка», чтобы отправить первую заявку.</div>
    <?php else: ?>
      <table>
        <thead>
        <tr>
          <th>Проект/мероприятие</th>
          <th>Дата</th>
          <th>Жанр</th>
          <th>Формат участия</th>
          <th>Статус</th>
        </tr>
        </thead>
        <tbody>
        <?php foreach ($requests as $request): ?>
          <tr>
            <td><?= htmlspecialchars($request['project_name']) ?></td>
            <td><?= htmlspecialchars($request['event_date']) ?></td>
            <td><?= htmlspecialchars($request['genre']) ?></td>
            <td><?= htmlspecialchars($request['participation_format']) ?></td>
            <td><span class="badge <?= statusClass($request['status']) ?>"><?= htmlspecialchars($request['status']) ?></span></td>
          </tr>
        <?php endforeach; ?>
        </tbody>
      </table>
    <?php endif; ?>
  </section>
</main>
</body>
</html>
