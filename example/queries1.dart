//
// Generated by 'sql2dart'
//

import 'package:sqflite/sqflite.dart';
Future<List<Map<String, dynamic>>> listMessages(Database db, sender,limit,offset,) async {
return await db.transaction((txn) async {
return await txn.rawQuery("""SELECT * FROM message WHERE sender =  ? ORDER BY sentAt LIMIT ? OFFSET ? """, [sender, limit, offset],);
});}