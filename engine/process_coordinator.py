import logging
import logging.handlers
import multiprocessing as mp
from datetime import datetime

import db.model
import db.query
import db.connection
from engine import simple_engine, simple_engine_rand, local_optimal


def _run(process, engine):
    logger = mp.get_logger()
    logger.setLevel(logging.INFO)
    handler = logging.handlers.RotatingFileHandler(
        filename='school_schedule.log', maxBytes=10000000, backupCount=5)
    bf = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(bf)
    logger.addHandler(handler)
    db.connection.connect()

    process.date_start = datetime.now()
    db.query.save(process)

    for x in range(1, process.cycles+1):
        logger.info(f'eseguo {process.kind} (run {x})')
        print(f'eseguo {process.kind} (run {x})')
        engine.run()
        if engine.closed:
            break
    if engine.closed:
        process.status = "CHIUSO"
    else:
        process.status = "APERTO"

    path = 'elaborazioni/calendario_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = path + '.csv'
    filename_debug = path + '_debug' + '.csv'
    engine.write_calendars_to_csv(filename=filename, filename_debug=filename_debug)

    file = db.model.File()
    file.filename = filename
    file_debug = db.model.File()
    file_debug.filename = filename_debug
    process.files.append(file)
    process.files.append(file_debug)
    process.date_end = datetime.now()
    db.query.save(process)
    db.connection.unconnect()

class ProcessCoordinator(object):
    process = None
    engine = None
    proc = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ProcessCoordinator, cls).__new__(cls)
        return cls.instance

    def start(self, process: db.model.Process):
        assert process is not None, "Invalid process to start"

        if self.is_running():
            logging.warning("A process is already running")
            return

        self.process = process
        options = {"Simple Engine": simple_engine.SimpleEngine,
                   "Randomized Engine": simple_engine_rand.SimpleEngineRand,
                   "Local Optimal Engine": local_optimal.LocalOptimalEngine}
        engine_class = options[self.process.kind]
        assert engine_class is not None, f'engine class unavailable for process kind {self.process.kind}'
        self.engine = engine_class()
        self.engine.load(school_year_id=self.process.school_year_id)
        for c in db.query.get_constraints(school_year_id=self.process.school_year_id):
            self.engine.add_constraint(c)
        self.process.status = "ESECUZIONE"
        self.proc = mp.Process(target=_run, args=(self.process, self.engine,))
        self.proc.start()
        logging.info(f'started process {process.kind}, id: {self.proc.name}')
        db.query.save(self.process)
#        p.join()

    def is_running(self):
        if self.proc is None:
            return False
        else:
            return self.proc.is_alive()

    def stop(self):
        assert self.proc is not None, "called stop with no process started"

        if self.proc.is_alive():
            self.proc.kill()
        self.proc.terminate()
        self.proc.close()
        self.proc.join()
        self.proc = None
