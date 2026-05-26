<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Docker Lab Work</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 40px 20px;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .container {
            max-width: 900px;
            width: 100%;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }
        .header h2 {
            margin: 10px 0 0;
            font-weight: 300;
            opacity: 0.9;
        }
        .content {
            padding: 40px;
        }
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .info-card {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            border-left: 4px solid #667eea;
        }
        .info-card h3 {
            margin: 0 0 15px 0;
            color: #333;
            font-size: 1.2em;
        }
        .info-card p {
            margin: 10px 0;
            color: #666;
        }
        .info-card .label {
            font-weight: bold;
            color: #333;
        }
        .success {
            color: #28a745;
            font-weight: bold;
        }
        .error {
            color: #dc3545;
            font-weight: bold;
        }
        .db-test {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
        }
        .db-test h3 {
            margin: 0 0 15px 0;
            color: #333;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #dee2e6;
        }
        th {
            background: #667eea;
            color: white;
            font-weight: 500;
        }
        tr:hover {
            background: #f5f5f5;
        }
        .footer {
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            border-top: 1px solid #dee2e6;
            color: #666;
        }
        .badge {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 0.9em;
            font-weight: 500;
        }
        .badge-success {
            background: #d4edda;
            color: #155724;
        }
        .badge-info {
            background: #d1ecf1;
            color: #0c5460;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1> Лабораторная работа №2</h1>
            <h2>Docker Compose: PHP + MySQL</h2>
        </div>
        
        <div class="content">
            <div class="info-grid">
                <div class="info-card">
                    <h3> Информация о контейнере</h3>
                    <p><span class="label">Container ID:</span> <code><?php echo gethostname(); ?></code></p>
                    <p><span class="label">Время работы:</span> <?php echo date('Y-m-d H:i:s'); ?></p>
                    <p><span class="label">PHP Version:</span> <?php echo phpversion(); ?></p>
                </div>
                
                <div class="info-card">
                    <h3>🔌 Информация о сети</h3>
                    <p><span class="label">Сервер MySQL:</span> <code>db</code></p>
                    <p><span class="label">Порт MySQL:</span> 3306</p>
                    <p><span class="label">База данных:</span> my_database</p>
                </div>
                
                <div class="info-card">
                    <h3> Статус подключения</h3>
                    <?php
                    $host = 'db';
                    $user = 'my_user';
                    $password = 'userpassword';
                    $database = 'my_database';
                    
                    $connection = new mysqli($host, $user, $password, $database);
                    
                    if ($connection->connect_error) {
                        echo "<p class='error'> Ошибка подключения: " . $connection->connect_error . "</p>";
                    } else {
                        echo "<p class='success'> Подключение к MySQL успешно!</p>";
                        echo "<p><span class='badge badge-success'>Соединение активно</span></p>";
                    }
                    ?>
                </div>
            </div>
            
            <div class="db-test">
                <h3> Тестирование базы данных</h3>
                <?php
                if (!$connection->connect_error) {
                    $createTable = "CREATE TABLE IF NOT EXISTS test_table (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )";
                    
                    if ($connection->query($createTable) === TRUE) {
                        echo "<p class='success'>✓ Таблица 'test_table' создана или уже существует</p>";
                        
                        $testData = [
                            ['Тестовая запись 1'],
                            ['Тестовая запись 2'],
                            ['Тестовая запись 3']
                        ];
                        
                        foreach ($testData as $data) {
                            $insert = "INSERT IGNORE INTO test_table (name) VALUES ('$data[0]')";
                            $connection->query($insert);
                        }
                        
                        $result = $connection->query("SELECT * FROM test_table ORDER BY created_at DESC LIMIT 5");
                        
                        if ($result->num_rows > 0) {
                            echo "<table>";
                            echo "<tr><th>ID</th><th>Название</th><th>Дата создания</th></tr>";
                            
                            while($row = $result->fetch_assoc()) {
                                echo "<tr>";
                                echo "<td>" . $row['id'] . "</td>";
                                echo "<td>" . $row['name'] . "</td>";
                                echo "<td>" . $row['created_at'] . "</td>";
                                echo "</tr>";
                            }
                            
                            echo "</table>";
                        }
                    } else {
                        echo "<p class='error'>Ошибка создания таблицы: " . $connection->error . "</p>";
                    }
                    
                    $connection->close();
                }
                ?>
            </div>
            
            <div style="margin-top: 30px; text-align: center;">
                <span class="badge badge-info"> Контейнеры: 2 (PHP + MySQL)</span>
                <span class="badge badge-info"> Сеть: project_db-network</span>
                <span class="badge badge-info"> Том: project_db_data</span>
            </div>
        </div>
        
        <div class="footer">
            <p>© 2025 Лабораторная работа №2 | Вариант 24 | Docker Compose</p>
        </div>
    </div>
</body>
</html>