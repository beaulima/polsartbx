import logging
import os
import thelper

def create_session_subparser(subparsers, mode):

    ap = subparsers.add_parser(mode, help="creates a new session from a config file")
    ap.add_argument("cfg_path", type=str, help="path to the session configuration file")
    ap.add_argument("save_dir", type=str, help="path to the session output root directory")

def create_session(args):
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
    logger.info("creating new training session '%s'..." % session_name)
    thelper.utils.setup_globals(config)
    save_dir = thelper.utils.get_save_dir(save_dir, session_name, config)
    logger.debug("session will be saved at '%s'" % os.path.abspath(save_dir).replace("\\", "/"))
    task, train_loader, valid_loader, test_loader = thelper.data.create_loaders(config, save_dir)
    model = thelper.nn.create_model(config, task, save_dir=save_dir)
    loaders = (train_loader, valid_loader, test_loader)
    trainer = thelper.train.create_trainer(session_name, save_dir, config, model, task, loaders)
    logger.debug("starting trainer")
    if train_loader:
        trainer.train()
    else:
        trainer.eval()
    logger.debug("all done")
    return trainer.outputs

logger = logging.getLogger("pyatcortbx.apps.create_session")