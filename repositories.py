import os
import pathlib
import sqlite3
import models

current_path = pathlib.Path(os.getcwd())
DB_FILE = str(current_path.parent) + '/db/db.sqlite3'

class RepositoryI:
    """
    Interface for repository object
    """
    def save(self, payment: models.Payment):
        raise NotImplementedError

    def load(self):
        raise NotImplementedError

class  SQLiteRepository(RepositoryI): 
    def save(self, payment: models.Payment):
        """
        Save (or update) payment in database
        """
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()

        cursor.execute(
            '''
            INSERT OR REPLACE INTO payments (id, value, currency, transaction_id, created_at, status)
            VALUES (?, ?, ?, ?, ?, ?)
            ''',
            (payment.id, payment.money.get_value(), payment.money.get_currency(), payment.transaction_id, payment.created_at, payment.status)
        )
        
        connection.commit()
        connection.close()
    
    def load(self) -> models.Payment:
        """
        Returns:
            Tuple of all payment objects
        """
        connection = sqlite3.connect(DB_FILE)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute(
            'SELECT * FROM payments'
        )
        query_list = cursor.fetchall()

        all_payments = []
        
        for row in query_list:
            current_payment = models.Payment(
                value = row['value'],
                currency = row['currency'],
                transaction_id = row['transaction_id'],
                created_at = row['created_at'],
                status = row['status']
            )
            current_payment.id = row['id']

            all_payments.append(current_payment)

        connection.close()

        return tuple(all_payments)

