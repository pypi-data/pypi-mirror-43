import os
import copy
import shutil
import subprocess

from troncli import utils, json_store, xml_store
from troncli.constants import *


class Config:
    """handler for setup config files"""

    def __init__(self):
        self.root_path = os.getcwd()
        self.full_config = None
        self.sol_config = None
        self.event_config = None
        self.enable_event_services = False
        self.node_list = utils.Node()
        self.phrase = utils.Phrase()
        self.config_store = {}

    async def init(self, reset):
        """
        Load raw json config
        """
        # check init
        if not self.node_list.get()['init_ed']:
            utils.error_msg('Please initialize first!')
            utils.info_msg('To get more initialize info:')
            utils.msg('tron-cli init -h')
            exit()

        if reset != 'False':
            self.node_list.reset_config()
        self.full_config = copy.deepcopy(json_store.raw_config)
        self.sol_config = copy.deepcopy(json_store.raw_config)
        self.event_config = copy.deepcopy(json_store.raw_config)
        self.eventnode_db_properties = copy.deepcopy(json_store.raw_eventnode_mongodb_properties)
        self.gridapi_db_properties = copy.deepcopy(json_store.raw_gridapi_application_properties)
        self.logback_config = copy.deepcopy(xml_store.logback)
        _config_store = self.node_list.get()
        self.config_store = _config_store['config']
        utils.success_msg('config initialized')

    async def export(self):
        """
        Export properties config file
        """
        _target_file_path_full = self.root_path + NODES_DIR + FULL_NODE_DIR + FULL_CONFIG
        self.phrase.store_json2properties_to_file(self.full_config, _target_file_path_full)
        utils.success_msg('fullnode config file exported to: ')
        utils.msg(_target_file_path_full)

        _target_file_path_sol = self.root_path + NODES_DIR + SOLIDITY_NODE_DIR + SOL_CONFIG
        self.phrase.store_json2properties_to_file(self.sol_config, _target_file_path_sol)
        utils.success_msg('soliditynode config file exported to: ')
        utils.msg(_target_file_path_sol)

        _target_file_path_event = self.root_path + NODES_DIR + EVENT_NODE_DIR + EVENT_CONFIG
        self.phrase.store_json2properties_to_file(self.event_config, _target_file_path_event)
        utils.success_msg('eventnode config file exported to: ')
        utils.msg(_target_file_path_event)
        await self.update_config_store()

        """
        Export logback
        """
        _target_file_path_full = self.root_path + NODES_DIR + FULL_NODE_DIR + "/" + LOGBACK_XML
        self.phrase.str2xml_to_file(self.logback_config, _target_file_path_full)

        _target_file_path_sol = self.root_path + NODES_DIR + SOLIDITY_NODE_DIR + "/" + LOGBACK_XML
        self.phrase.str2xml_to_file(self.logback_config, _target_file_path_sol)

    async def update_config_store(self):
        await self.node_list.update_config(self.config_store['nettype'],
                                           self.config_store['fullhttpport'],
                                           self.config_store['solhttpport'],
                                           self.config_store['eventhttpport'],
                                           self.config_store['fullrpcport'],
                                           self.config_store['solrpcport'],
                                           self.config_store['eventrpcport'],
                                           self.config_store['enablememdb'],
                                           self.config_store['dbsyncmode'],
                                           self.config_store['saveintertx'],
                                           self.config_store['savehistorytx'],
                                           self.config_store['gridport'],
                                           self.config_store['dbname'],
                                           self.config_store['dbusername'],
                                           self.config_store['dbpassword'])

    async def set_http_port(self, port_num, node_type, net_type):
        if node_type == 'full':
            # check void and restore
            if port_num == 0:
                port_num = self.config_store['fullhttpport']
            else:
                self.config_store['fullhttpport'] = port_num

            self.full_config[' node'][' http'][' fullNodePort'] = port_num
            if net_type == 'private':
                self.event_config[' seed.node'][' ip.list'] = [LOCAL_HOST + str(port_num)]
                self.event_config[' node'][' active'] = [LOCAL_HOST + str(port_num)]
            utils.success_msg('full-node http request set to listen: ')
            utils.msg(LOCAL_HOST + str(port_num))
        elif node_type == 'sol':
            # check void and restore
            if port_num == 0:
                port_num = self.config_store['solhttpport']
            else:
                self.config_store['solhttpport'] = port_num

            self.sol_config[' node'][' http'][' solidityPort'] = port_num
            utils.success_msg('solidity-node request set to listen: ')
            utils.msg(LOCAL_HOST + str(port_num))
        elif node_type == 'event':
            # check void and restore
            if port_num == 0:
                port_num = self.config_store['eventhttpport']
            else:
                self.config_store['eventhttpport'] = port_num

            self.event_config[' node'][' http'][' fullNodePort'] = port_num
            utils.success_msg('event-node request set to listen: ')
            utils.msg(LOCAL_HOST + str(port_num))
        else:
            utils.warning_msg('wrong node_type')

    async def set_rpc_port(self, port_num, node_type):
        if node_type == 'full':
            # check void and restore
            if port_num == 0:
                port_num = self.config_store['fullrpcport']
            else:
                self.config_store['fullrpcport'] = port_num

            self.full_config[' node'][' rpc'][' port'] = port_num
            self.sol_config[' node'][' trustNode'] = LOCAL_HOST + str(port_num)
            utils.success_msg('full-node rpc request set to listen: ')
            utils.msg(LOCAL_HOST + str(port_num))
        elif node_type == 'sol':
            # check void and restore
            if port_num == 0:
                port_num = self.config_store['solrpcport']
            else:
                self.config_store['solrpcport'] = port_num

            self.sol_config[' node'][' rpc'][' port'] = port_num
            utils.success_msg('solidity-node rpc request set to listen: ')
            utils.msg(LOCAL_HOST + str(port_num))
        elif node_type == 'event':
            # check void and restore
            if port_num == 0:
                port_num = self.config_store['eventrpcport']
            else:
                self.config_store['eventrpcport'] = port_num

            self.event_config[' node'][' rpc'][' port'] = port_num
            utils.success_msg('event-node rpc request set to listen: ')
            utils.msg(LOCAL_HOST + str(port_num))
        else:
            utils.warning_msg('wrong node_type')

    async def set_net_type(self, net_type):
        # check void and restore
        if net_type == '':
            net_type = self.config_store['nettype']
        else:
            self.config_store['nettype'] = net_type

        # msg
        utils.success_msg('net type set to: ')
        utils.msg(net_type)
        # P2P verison
        if net_type == 'main':
            self.full_config[' node'][' p2p'][' version'] = MAINNET_P2P_VERSION
            self.sol_config[' node'][' p2p'][' version'] = MAINNET_P2P_VERSION
            self.event_config[' node'][' p2p'][' version'] = MAINNET_P2P_VERSION
        if net_type == 'private':
            self.full_config[' node'][' p2p'][' version'] = PRIVATENET_P2P_VERSION
            self.sol_config[' node'][' p2p'][' version'] = PRIVATENET_P2P_VERSION
            self.event_config[' node'][' p2p'][' version'] = PRIVATENET_P2P_VERSION
        # committee
        
        # vm
        if net_type == 'main':
            self.full_config[' vm'][' supportConstant'] = 'false'
            self.sol_config[' vm'][' supportConstant'] = 'false'
            self.event_config[' vm'][' supportConstant'] = 'false'
        if net_type == 'private':
            self.full_config[' vm'][' supportConstant'] = 'true'
            self.sol_config[' vm'][' supportConstant'] = 'true'
            self.event_config[' vm'][' supportConstant'] = 'true'
        # block
        if net_type == 'main':
            self.full_config[' block'][' needSyncCheck'] = 'true'
            self.sol_config[' block'][' needSyncCheck'] = 'true'
            self.event_config[' block'][' needSyncCheck'] = 'true'
        if net_type == 'private':
            self.full_config[' block'][' needSyncCheck'] = 'false'
            self.sol_config[' block'][' needSyncCheck'] = 'false'
            self.event_config[' block'][' needSyncCheck'] = 'false'
        # localwitness
        if net_type == 'main':
            self.full_config[' localwitness'] = []
            self.sol_config[' localwitness'] = []
            self.event_config[' localwitness'] = []
        if net_type == 'private':
            self.full_config[' localwitness'] = [TEST_ACCOUNT_PK]
            self.sol_config[' localwitness'] = [TEST_ACCOUNT_PK]
            self.event_config[' localwitness'] = [TEST_ACCOUNT_PK]
        # genesis.block
        if net_type == 'main':
            genesis_block_parent_hash = '0xe58f33f9baf9305dc6f82b9f1934ea8f0ade2defb951258d50167028c780351f'
            self.full_config[' genesis.block'][' parentHash'] = genesis_block_parent_hash
            self.sol_config[' genesis.block'][' parentHash'] = genesis_block_parent_hash
            self.event_config[' genesis.block'][' parentHash'] = genesis_block_parent_hash
        if net_type == 'private':
            # add witnesses
            self.full_config[' genesis.block'][' witnesses'] = [{
                ' address': TEST_ACCOUNT_ADDRESS,
                ' url': 'https://github.com/tronprotocol/tron-cli',
                ' voteCount': 10000}]
            # add assets
            self.full_config[' genesis.block'][' assets'] = [{
                ' accountName': 'TRONCLI',
                ' accountType': 'AssetIssue',
                ' address': TEST_ACCOUNT_ADDRESS,
                ' balance': 9000000000000000},
                {
                ' accountName': 'Sun',
                ' accountType': 'AssetIssue',
                ' address': 'TXmVpin5vq5gdZsciyyjdZgKRUju4st1wM',
                ' balance': 5000000000000000},
                {
                ' accountName': 'Blackhole',
                ' accountType': 'AssetIssue',
                ' address': 'TLsV52sRDL79HXGGm9yzwKibb6BeruhUzy',
                ' balance': -9223372036854775808}]

    async def set_db_version(self, enablememdb):
        # check void and restore
        if enablememdb == '':
            enablememdb = self.config_store['enablememdb']
        else:
            self.config_store['enablememdb'] = enablememdb

        if enablememdb == 'disable' or enablememdb == '0' or enablememdb == 'False':
            self.full_config[' storage'][' db.version'] = DB_DISK_ONLY_VERSION
            self.event_config[' storage'][' db.version'] = DB_DISK_ONLY_VERSION
            utils.success_msg('enable in memory db:')
            utils.msg('False')
        else:
            self.full_config[' storage'][' db.version'] = DB_IN_MEMORY_SUPPORT_VERSION
            self.event_config[' storage'][' db.version'] = DB_IN_MEMORY_SUPPORT_VERSION
            utils.success_msg('enable in memory db:')
            utils.msg('True')

    async def store_db_settings(self, dbname, dbusername, dbpassword, gridport):
        # check void and restore
        if dbname == 'Null':
            dbname = self.config_store['dbname']
        else:
            self.config_store['dbname'] = dbname

        if dbusername == 'Null':
            dbusername = self.config_store['dbusername']
        else:
            self.config_store['dbusername'] = dbusername

        if dbpassword == 'Null':
            dbpassword = self.config_store['dbpassword']
        else:
            self.config_store['dbpassword'] = dbpassword

        if gridport == 0:
            gridport = self.config_store['gridport']
        else:
            self.config_store['gridport'] = gridport
            utils.success_msg('grid api http request set to listen: ')
            utils.msg(LOCAL_HOST + str(gridport))
        await self.update_config_store()

        if dbname == 'Null' and dbusername == 'Null' and dbpassword == 'Null':
            self.enable_event_services = False
            utils.warning_msg('Not configing event services since db settings not specified.')
            utils.info_msg(
                'config event services by specify --dbname <name> --dbusername <user> --dbpassword <password>')
        elif dbname == 'Null':
            utils.error_msg('Please set db name with --dbname')
            exit()
        elif dbusername == 'Null':
            utils.error_msg('Please set db user name with --dbusername')
            exit()
        elif dbpassword == 'Null':
            utils.error_msg('Please set db password with --dbpassword')
            exit()
        else:
            self.enable_event_services = True
            await self.node_list.update_db_settings(dbname, dbusername, dbpassword)
            utils.success_msg('db settings stored')
            await self.change_eventnode_db_settings()
            await self.change_gridapi_db_settings(gridport)
            await self.build_eventnode_jar()
            await self.build_gridapi_jar()
            await self.move_gridapi_jar()

    async def change_eventnode_db_settings(self):
        _db = self.node_list.get()
        # utils.debug(str(_db['db']))
        self.eventnode_db_properties[' mongo.dbname'] = _db['db']['dbname']
        self.eventnode_db_properties[' mongo.username'] = _db['db']['dbusername']
        self.eventnode_db_properties[' mongo.password'] = _db['db']['dbpassword']
        """
        export
        """
        _target_file_path_sol = self.root_path + NODES_DIR + EVENT_NODE_DIR + '/src/main/resources/mongodb.properties'
        self.phrase.store_json2javabeanconfig_to_file(self.eventnode_db_properties, _target_file_path_sol)
        utils.success_msg('changed db settings for event node at: ')
        utils.msg(_target_file_path_sol)

    async def change_gridapi_db_settings(self, gridport):
        _db = self.node_list.get()
        # utils.debug(str(_db['db']))
        self.gridapi_db_properties[' spring.data.mongodb.database'] = _db['db']['dbname']
        self.gridapi_db_properties[' spring.data.mongodb.username'] = _db['db']['dbusername']
        self.gridapi_db_properties[' spring.data.mongodb.password'] = _db['db']['dbpassword']
        self.gridapi_db_properties[' server.port'] = gridport
        utils.success_msg('grid api request set to listen: ')
        utils.msg(LOCAL_HOST + str(gridport))
        """
        export
        """
        _target_file_path_sol = self.root_path + NODES_DIR + GRID_API_DIR + '/src/main/resources/application.properties'
        self.phrase.store_json2javabeanconfig_to_file(self.gridapi_db_properties, _target_file_path_sol)
        # utils.success_msg('changed db settings for grid api at: ')
        # utils.msg(_target_file_path_sol)

    async def build_gridapi_jar(self):
        utils.progress_msg('Build grid api jar')
        os.chdir(self.root_path + NODES_DIR + GRID_API_DIR)
        subprocess.call(['mvn', 'package'])
        os.chdir(self.root_path)

    async def move_gridapi_jar(self):
        utils.success_msg('grid api jar move to:')
        shutil.move(self.root_path + NODES_DIR + GRID_API_DIR + '/target/trongrid-' + TRON_GRID_VERSION + '-SNAPSHOT.jar',
                    self.root_path + NODES_DIR + GRID_API_DIR + GRID_NODE_JAR)
        utils.msg(self.root_path + NODES_DIR + GRID_API_DIR + GRID_NODE_JAR)

    async def build_eventnode_jar(self):
        utils.progress_msg('Build event node jar')
        os.chdir(self.root_path + NODES_DIR + EVENT_NODE_DIR)
        await utils.gradlew_build('event node')
        os.chdir(self.root_path)
        shutil.move(self.root_path + NODES_DIR + EVENT_NODE_DIR + '/build/libs/FullNode.jar',
                    self.root_path + NODES_DIR + EVENT_NODE_DIR + EVENT_NODE_JAR)
        utils.success_msg('event node jar move to:')
        utils.msg(self.root_path + NODES_DIR + EVENT_NODE_DIR + EVENT_NODE_JAR)

    async def set_db_sync_mode(self, dbsyncmode):
        # check void and restore
        if dbsyncmode == '':
            dbsyncmode = self.config_store['dbsyncmode']
        else:
            self.config_store['dbsyncmode'] = dbsyncmode

        if dbsyncmode == 'async':
            self.full_config[' storage'][' db.sync'] = 'false'
            self.sol_config[' storage'][' db.sync'] = 'false'
            self.event_config[' storage'][' db.sync'] = 'false'
            utils.success_msg('db sync mode set to: ')
            utils.msg('asynchronous')
        elif dbsyncmode == 'sync':
            self.full_config[' storage'][' db.sync'] = 'true'
            self.sol_config[' storage'][' db.sync'] = 'true'
            self.event_config[' storage'][' db.sync'] = 'true'
            utils.success_msg('db sync mode set to: ')
            utils.msg('synchronous')
        else:
            utils.warning_msg('wrong dbsyncmode, expect async or sync, however ' + dbsyncmode + ' is given')

    async def enable_save_inter_tx(self, saveintertx):
        # check void and restore
        if saveintertx == '':
            saveintertx = self.config_store['saveintertx']
        else:
            self.config_store['saveintertx'] = saveintertx

        if saveintertx == 'enable' or saveintertx == '1' or saveintertx == 'True' or saveintertx == 'on':
            self.full_config[' vm'][' saveInternalTx'] = 'true'
            self.sol_config[' vm'][' saveInternalTx'] = 'true'
            self.event_config[' vm'][' saveInternalTx'] = 'true'
            utils.success_msg('save history transaction: ')
            utils.msg('enabled')
        else:
            self.full_config[' vm'][' saveInternalTx'] = 'false'
            self.sol_config[' vm'][' saveInternalTx'] = 'false'
            self.event_config[' vm'][' saveInternalTx'] = 'false'
            utils.success_msg('save history transaction: ')
            utils.msg('disabled')

    async def enable_save_history_tx(self, savehistorytx):
        # check void and restore
        if savehistorytx == '':
            savehistorytx = self.config_store['savehistorytx']
        else:
            self.config_store['savehistorytx'] = savehistorytx

        if savehistorytx == 'enable' or savehistorytx == '1' or savehistorytx == 'True' or savehistorytx == 'on':
            self.full_config[' storage'][' transHistory.switch'] = 'on'
            self.sol_config[' storage'][' transHistory.switch'] = 'on'
            self.event_config[' storage'][' transHistory.switch'] = 'on'
            utils.success_msg('save internal transaction: ')
            utils.msg('enabled')
        else:
            self.full_config[' storage'][' transHistory.switch'] = 'off'
            self.sol_config[' storage'][' transHistory.switch'] = 'off'
            self.event_config[' storage'][' transHistory.switch'] = 'off'
            utils.success_msg('save internal transaction: ')
            utils.msg('disabled')
