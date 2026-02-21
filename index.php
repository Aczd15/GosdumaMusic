<?php

declare(strict_types=1);

require_once __DIR__ . '/auth.php';

if (currentUser()) {
    header('Location: dashboard.php');
    exit;
}

$error = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $login = trim($_POST['login'] ?? '');
    $password = $_POST['password'] ?? '';

    if ($login === '' || $password === '') {
        $error = 'Введите логин и пароль.';
    } elseif (isAdmin($login, $password)) {
        $_SESSION['is_admin'] = true;
        header('Location: admin.php');
        exit;
    } else {
        $stmt = db()->prepare('SELECT * FROM users WHERE login = :login');
        $stmt->execute(['login' => $login]);
        $user = $stmt->fetch();

        if (!$user || !password_verify($password, $user['password_hash'])) {
            $error = 'Неверный логин или пароль.';
        } else {
            $_SESSION['user_id'] = (int) $user['id'];
            unset($_SESSION['is_admin']);
            header('Location: dashboard.php');
            exit;
        }
    }
}
?>
<!doctype html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GosdumaMusic — Авторизация</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <main class="container">
    <section class="card" style="max-width: 520px; margin: 40px auto;">
      <h1>GosdumaMusic</h1>
      <p class="helper">Вход в систему для пользователей и администратора.</p>
      <?php if ($error): ?>
        <div class="message message-error"><?= htmlspecialchars($error) ?></div>
      <?php endif; ?>
      <form method="post" novalidate>
        <label>
          Логин
          <input type="text" name="login" required>
        </label>
        <label>
          Пароль
          <input type="password" name="password" required>
        </label>
        <button class="btn btn-primary" type="submit">Войти</button>
      </form>
      <p style="margin-top: 12px;">Еще не зарегистрированы? <a href="register.php">Регистрация</a></p>
    </section>
  </main>
</body>
</html>
