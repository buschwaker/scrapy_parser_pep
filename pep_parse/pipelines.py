import csv
import time

from .settings import BASE_DIR


class PepParsePipeline:

    def open_spider(self, spider):
        self.SEEN_STATUSES = {
            'Active': 0,
            'Accepted': 0,
            'Deferred': 0,
            'Final': 0,
            'Provisional': 0,
            'Rejected': 0,
            'Superseded': 0,
            'Withdrawn': 0,
            'Draft': 0,
            'April Fool!': 0,
            'Total': 0
        }

    def process_item(self, item, spider):
        status = item['status']
        self.SEEN_STATUSES[status] = self.SEEN_STATUSES.get(status, 0) + 1
        return item

    def close_spider(self, spider):
        results_dir = BASE_DIR / 'results'
        results_dir.mkdir(exist_ok=True)
        filename = (
            f'status_summary_{time.strftime("%Y-%m-%d_%H-%M-%S")}.csv'
        )
        file_path = results_dir / filename
        self.SEEN_STATUSES['Total'] = sum(self.SEEN_STATUSES.values())
        special_format_for_writing = [
            [
                'Статус', 'Количество'
            ] + [k, v] for k, v in self.SEEN_STATUSES.items()
        ]
        with open(file_path, mode='w', encoding='utf-8') as f:
            writer = csv.writer(f, dialect='unix')
            writer.writerows(special_format_for_writing)
