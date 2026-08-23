<?php
/**
 * Newsletter subscribe relay: POST /api/subscribe -> Brevo Contacts API.
 * Brevo API key is stored OUTSIDE the web root (../../brevo-api-key).
 * Request : {"email": "...", "name": "..."}  (+ optional honeypot "website")
 * Response: {"success": true} | {"success": false, "error": "..."}
 */
header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');

function respond($status, $payload) {
    http_response_code($status);
    echo json_encode($payload);
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    respond(405, ['success' => false, 'error' => 'Method not allowed']);
}

$data = json_decode((string)file_get_contents('php://input'), true);
if (!is_array($data)) {
    respond(400, ['success' => false, 'error' => 'Du lieu khong hop le.']);
}

// Honeypot: bots fill every field — drop silently, pretend success.
if (!empty($data['website'])) {
    respond(200, ['success' => true]);
}

$email = isset($data['email']) ? trim((string)$data['email']) : '';
$name  = isset($data['name']) ? trim((string)$data['name']) : '';

if (!filter_var($email, FILTER_VALIDATE_EMAIL) || strlen($email) > 254) {
    respond(400, ['success' => false, 'error' => 'Email không hợp lệ.']);
}
if (function_exists('mb_substr')) {
    $name = mb_substr($name, 0, 100);
} else {
    $name = substr($name, 0, 100);
}

// Rate limit: max 5 requests/hour/IP (file-based, good enough for a blog).
$ip   = $_SERVER['HTTP_CF_CONNECTING_IP'] ?? $_SERVER['REMOTE_ADDR'] ?? 'unknown';
$slot = sys_get_temp_dir() . '/sub_rl_' . md5((string)$ip) . '.json';
$now  = time();
$hits = [];
if (is_file($slot)) {
    $decoded = json_decode((string)file_get_contents($slot), true);
    if (is_array($decoded)) {
        foreach ($decoded as $t) {
            if (is_int($t) && $t > $now - 3600) { $hits[] = $t; }
        }
    }
}
if (count($hits) >= 5) {
    respond(429, ['success' => false, 'error' => 'Quá nhiều yêu cầu. Vui lòng thử lại sau.']);
}
$hits[] = $now;
file_put_contents($slot, json_encode($hits), LOCK_EX);

// Brevo API key — outside the web root, never committed to the repo.
$keyFile = dirname(__DIR__, 2) . '/brevo-api-key';
$apiKey  = is_readable($keyFile) ? trim((string)file_get_contents($keyFile)) : '';
if ($apiKey === '') {
    respond(500, ['success' => false, 'error' => 'Có lỗi xảy ra. Vui lòng thử lại.']);
}

$payload = json_encode([
    'email'         => $email,
    'attributes'    => ['FIRSTNAME' => $name],
    'updateEnabled' => true,
]);

$ch = curl_init('https://api.brevo.com/v3/contacts');
curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_POST           => true,
    CURLOPT_POSTFIELDS     => $payload,
    CURLOPT_HTTPHEADER     => [
        'accept: application/json',
        'content-type: application/json',
        'api-key: ' . $apiKey,
    ],
    CURLOPT_CONNECTTIMEOUT => 8,
    CURLOPT_TIMEOUT        => 15,
]);
$response = curl_exec($ch);
$status   = (int)curl_getinfo($ch, CURLINFO_HTTP_CODE);
$errno    = curl_errno($ch);
curl_close($ch);

if ($errno !== 0 || $response === false) {
    respond(502, ['success' => false, 'error' => 'Không kết nối được dịch vụ. Vui lòng thử lại.']);
}
if ($status >= 200 && $status < 300) {
    respond(200, ['success' => true]);
}
// Never echo upstream body (may contain PII) — generic error only.
respond(502, ['success' => false, 'error' => 'Có lỗi xảy ra. Vui lòng thử lại.']);
