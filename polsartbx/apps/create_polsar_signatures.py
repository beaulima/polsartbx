import logging
import os
import thelper

logger = logging.getLogger("pyatcortbx.apps.create_polsar_signatures")


def create_polsar_signatures_subparser(subparsers, mode):

    ap = subparsers.add_parser(mode, help="creates a new session from a config file")
    ap.add_argument("cfg_path", type=str, help="path to the session configuration file")
    ap.add_argument("save_dir", type=str, help="path to the session output root directory")

def create_polsar_signatures(args):
    """Creates a session to train a model.

    All generated outputs (model checkpoints and logs) will be saved in a directory named after the
    session (the name itself is specified in ``config``), and located in ``save_dir``.

    Args:
        args: input arguments must contain:
            - args.cfg_path, the path to the config dictionary that provides all required data configuration and
            trainer parameters; see:class:`thelper.train.base.Trainer` and :func:`thelper.data.utils.create_loaders`
            for more information. Here, it is only expected to contain a ``name`` field that specifies the name of
            the session.
            - args.save_dir, the path to the root directory where the session directory should be saved. Note that
            this is not the path to the session directory itself, but its parent, which may also contain
            other session directories.

    .. seealso::
        | :class:`thelper.train.base.Trainer`
    """
    logger = thelper.utils.get_func_logger()

    config = thelper.utils.load_config(args.cfg_path)
    save_dir = args.save_dir

    session_name = thelper.utils.get_config_session_name(config)
    assert session_name is not None, "config missing 'name' field required for output directory"
    logger.info("creating new polsar signatures creation session '%s'..." % session_name)

    toto = 0





