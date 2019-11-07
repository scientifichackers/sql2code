insertMessage(type, text) {
    INSERT INTO message(type, text) VALUES($type, $text);
}
