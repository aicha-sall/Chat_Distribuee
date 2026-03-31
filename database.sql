-- ========================================
-- Base de données – Chat Distribué DEVNET
-- ========================================

CREATE DATABASE IF NOT EXISTS chat_distribue
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE chat_distribue;

-- ── Table utilisateurs ────────────────────
CREATE TABLE IF NOT EXISTS utilisateurs (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    username     VARCHAR(50) UNIQUE NOT NULL,
    service_name VARCHAR(50) NOT NULL,
    port         INT NOT NULL,
    created_at   DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_username (username)
);

-- ── Table messages ────────────────────────
CREATE TABLE IF NOT EXISTS messages (
    id                 INT AUTO_INCREMENT PRIMARY KEY,
    content            TEXT NOT NULL,
    sender_id          INT NOT NULL,
    receiver_id        INT NULL,
    service_expediteur VARCHAR(50) NOT NULL,
    created_at         DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id)   REFERENCES utilisateurs(id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES utilisateurs(id) ON DELETE SET NULL,
    INDEX idx_sender    (sender_id),
    INDEX idx_receiver  (receiver_id),
    INDEX idx_created   (created_at)
);

-- ── Données de test ───────────────────────
INSERT INTO utilisateurs (username, service_name, port) VALUES
('Alice',            'service_1', 5000),
('Bob',              'service_2', 5001),
('User_5000',        'service_1', 5000),
('User_5001',        'service_2', 5001);

INSERT INTO messages (content, sender_id, receiver_id, service_expediteur) VALUES
('Bonjour Bob !',              1, 2,    'service_1'),
('Salut Alice !',              2, 1,    'service_2'),
('Comment ça va ?',            1, 2,    'service_1'),
('Très bien merci !',          2, 1,    'service_2'),
('Message pour tout le monde', 3, NULL, 'service_1'),
('Autre message de test',      4, NULL, 'service_2');

-- ── Vérification ─────────────────────────
SELECT 'Base chat_distribue créée avec succès !' AS statut;
SELECT * FROM utilisateurs;
SELECT m.id, m.content, u1.username AS expediteur,
       u2.username AS destinataire, m.service_expediteur, m.created_at
FROM messages m
LEFT JOIN utilisateurs u1 ON m.sender_id   = u1.id
LEFT JOIN utilisateurs u2 ON m.receiver_id = u2.id
ORDER BY m.created_at DESC;
