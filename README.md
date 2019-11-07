# SQL 2 code

This project lets you write functions in SQL and import them in code.  

Currently, it only supports dart.

```sql
-- queries1.sql
listMessages(sender, limit, offset) {
    SELECT *
      FROM message
     WHERE sender = $sender  
  ORDER BY sentAt
     LIMIT $limit OFFSET $offset;
}
```

```console
$ sql2dart quries.sql queries.dart 
```

```dart
// queries.dart
import 'package:sqflite/sqflite.dart';

Future<List<Map<String, dynamic>>> listMessages(
  Database db,
  sender,
  limit,
  offset,
) async {
  return await db.transaction((txn) async {
    return await txn.rawQuery(
      """SELECT * FROM message WHERE sender =  ? ORDER BY sentAt LIMIT ? OFFSET ? """,
      [sender, limit, offset],
    );
  });
}
```