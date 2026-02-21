<?php

declare(strict_types=1);

require_once __DIR__ . '/auth.php';

requireAdmin();

$statuses = ['Новая', 'На рассмотрении', 'Одобрена', 'Отклонена'];

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $id = (int) ($_POST['request_id'] ?? 0);
    $status = trim($_POST['status'] ?? '');

    if ($id > 0 && in_array($status, $statuses, true)) {
        $stmt = db()->prepare('UPDATE requests SET status = :status WHERE id = :id');
        $stmt->execute(['status' => $status, 'id' => $id]);
    }

    header('Location: admin.php');
    exit;
}

$stmt = db()->query('SELECT r.*, u.login, u.full_name
FROM requests r
JOIN users u ON u.id = r.user_id
ORDER BY r.id DESC');
$requests = $stmt->fetchAll();
?>
<!doctype html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GosdumaMusic — Панель администратора</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
<main class="container">
  <header class="nav">
    <h1>Панель администратора</h1>
    <a class="btn btn-primary" href="logout.php">Выйти</a>
  </header>
  <section class="card">
    <h2>Все заявки пользователей</h2>
    <?php if (!$requests): ?>
      <p class="helper">Пока заявок нет.</p>
    <?php else: ?>
      <table>
        <thead>
        <tr>
          <th>Пользователь</th>
          <th>Проект</th>
          <th>Дата</th>
          <th>Жанр</th>
          <th>Формат</th>
          <th>Статус</th>
        </tr>
        </thead>
        <tbody>
        <?php foreach ($requests as $request): ?>
          <tr>
            <td><?= htmlspecialchars($request['full_name']) ?> (<?= htmlspecialchars($request['login']) ?>)</td>
            <td><?= htmlspecialchars($request['project_name']) ?></td>
            <td><?= htmlspecialchars($request['event_date']) ?></td>
            <td><?= htmlspecialchars($request['genre']) ?></td>
            <td><?= htmlspecialchars($request['participation_format']) ?></td>
            <td>
              <form method="post">
                <input type="hidden" name="request_id" value="<?= (int) $request['id'] ?>">
                <select name="status" onchange="this.form.submit()">
                  <?php foreach ($statuses as $status): ?>
                    <option value="<?= htmlspecialchars($status) ?>" <?= $request['status'] === $status ? 'selected' : '' ?>><?= htmlspecialchars($status) ?></option>
                  <?php endforeach; ?>
                </select>
              </form>
            </td>
          </tr>
        <?php endforeach; ?>
        </tbody>
      </table>
    <?php endif; ?>
  </section>
</main>
</body>
</html>
