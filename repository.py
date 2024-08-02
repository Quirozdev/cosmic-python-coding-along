import abc
import model


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, batch: model.Batch):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference) -> model.Batch:
        raise NotImplementedError


class SqlRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, batch):
        self.session.execute('INSERT INTO batches (reference, sku, _purchased_quantity, eta) VALUES (:reference, :sku, :_purchased_quantity, :eta)', dict(reference=batch.reference, sku=batch.sku, _purchased_quantity=batch._purchased_quantity, eta=batch.eta))
        rows = self.session.execute('SELECT id FROM batches WHERE reference = :reference', dict(reference=batch.reference))
        batch_id = list(rows)[0]['id']

        for orderline in batch._allocations:
            self.session.execute('INSERT INTO order_lines (sku, qty, orderid) VALUES (:sku, :qty, :orderid)', dict(sku=orderline.sku, qty=orderline.qty, orderid=orderline.orderid))
            rows = self.session.execute('SELECT id FROM order_lines WHERE sku = :sku AND qty = :qty AND orderid = :orderid', dict(sku=orderline.sku, qty=orderline.qty, orderid=orderline.orderid))
            orderline_id = list(rows)[0]['id']
            self.session.execute('INSERT INTO allocations (orderline_id, batch_id) VALUES (:orderline_id, :batch_id)', dict(orderline_id=orderline_id, batch_id=batch_id))

    def get(self, reference) -> model.Batch:
        rows = self.session.execute('SELECT * FROM batches WHERE reference = :reference', dict(reference=reference))
        batch_tuple = list(rows)[0]
        allocation_rows = self.session.execute('SELECT orderid, sku, qty FROM allocations JOIN order_lines ON allocations.orderline_id = order_lines.id WHERE batch_id = :batch_id', dict(batch_id=batch_tuple['id']))
        
        batch = model.Batch(batch_tuple.reference, batch_tuple.sku, batch_tuple._purchased_quantity, batch_tuple.eta)
        for row in allocation_rows:
            order_line = model.OrderLine(row.orderid, row.sku, row.qty)
            batch.allocate(order_line)
        return batch
    