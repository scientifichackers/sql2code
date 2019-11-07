listMessages(sender, limit, offset) {
    SELECT *
      FROM message
     WHERE sender = $sender
  ORDER BY sentAt
     LIMIT $limit OFFSET $offset;
}