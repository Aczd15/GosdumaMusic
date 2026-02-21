<?php

declare(strict_types=1);

require_once __DIR__ . '/auth.php';

if (currentUser()) {
    header('Location: dashboard.php');
    exit;
}

$errors = [];
$success = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $login = trim($_POST['login'] ?? '');
    $password = $_POST['password'] ?? '';
    $fullName = trim($_POST['full_name'] ?? '');
    $phone = trim($_POST['phone'] ?? '');
    $email = trim($_POST['email'] ?? '');

    if ($login === '' || mb_strlen($login) < 3) {
        $errors[] = 'Логин обязателен и должен содержать минимум 3 символа.';
    }

    if ($password === '' || mb_strlen($password) < 6) {
        $errors[] = 'Пароль обязателен и должен содержать минимум 6 символов.';
    }

    if (!preg_match('/^[А-Яа-яЁё\s]+$/u', $fullName)) {
        $errors[] = 'ФИО должно содержать только кириллицу и пробелы.';
    }

    if (!preg_match('/^8\(\d{3}\)\d{3}-\d{2}-\d{2}$/', $phone)) {
        $errors[] = 'Телефон должен быть в формате 8(XXX)XXX-XX-XX.';
    }

    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $errors[] = 'Введите корректный e-mail.';
    }

    $check = db()->prepare('SELECT COUNT(*) FROM users WHERE login = :login OR email = :email');
    $check->execute(['login' => $login, 'email' => $email]);
    if ((int) $check->fetchColumn() > 0) {
        $errors[] = 'Пользователь с таким логином или e-mail уже существует.';
    }

    if (empty($errors)) {
        $stmt = db()->prepare('INSERT INTO users (login, password_hash, full_name, phone, email, created_at)
            VALUES (:login, :password_hash, :full_name, :phone, :email, :created_at)');
        $stmt->execute([
            'login' => $login,
            'password_hash' => password_hash($password, PASSWORD_DEFAULT),
            'full_name' => $fullName,
            'phone' => $phone,
            'email' => $email,
            'created_at' => date('c'),
        ]);
        $success = 'Регистрация прошла успешно. Теперь вы можете войти.';
    }
}
?>
<!doctype html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GosdumaMusic — Регистрация</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
<main class="container">
  <section class="card" style="max-width: 620px; margin: 30px auto;">
    <h1>Регистрация в GosdumaMusic</h1>
    <p class="helper">Заполните все обязательные поля.</p>
    <?php foreach ($errors as $error): ?>
      <div class="message message-error" style="margin-bottom: 8px;"><?= htmlspecialchars($error) ?></div>
    <?php endforeach; ?>
    <?php if ($success): ?>
      <div class="message message-success"><?= htmlspecialchars($success) ?></div>
    <?php endif; ?>
    <form method="post" novalidate>
      <label>Логин
        <input type="text" name="login" required value="<?= htmlspecialchars($_POST['login'] ?? '') ?>">
      </label>
      <label>Пароль
        <input type="password" name="password" required>
      </label>
      <label>ФИО
        <input type="text" name="full_name" required value="<?= htmlspecialchars($_POST['full_name'] ?? '') ?>">
      </label>
      <label>Телефон (8(XXX)XXX-XX-XX)
        <input type="text" name="phone" required placeholder="8(999)123-45-67" value="<?= htmlspecialchars($_POST['phone'] ?? '') ?>">
      </label>
      <label>E-mail
        <input type="email" name="email" required value="<?= htmlspecialchars($_POST['email'] ?? '') ?>">
      </label>
      <button class="btn btn-primary" type="submit">Зарегистрироваться</button>
    </form>
    <p style="margin-top: 12px;">Уже зарегистрированы? <a href="index.php">Авторизация</a></p>
  </section>
</main>
</body>
</html>
