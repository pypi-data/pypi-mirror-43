from LbSoftConfDB.SoftConfDB import SoftConfDB as oldSoftConfDb
from LbSoftConfDb2Server.SoftConfDB import SoftConfDB as newSoftConfDb, \
    get_connection
from LbSoftConfDb2Server.LbSoftConfDbObjects import Platform
import os
import sys
from datetime import datetime
import time

class LbSoftConfDbMigration:

    def __init__(self):
        os.environ['NEO4JHOST'] = 'lbsoftdb.cern.ch'
        self.old_db = oldSoftConfDb()
        self.new_db = newSoftConfDb(get_connection())
        self.new_db.mNeoDB.delete_all()
        self.errors = []

    def start(self):
        all_projects = self.old_db.listProjects()
        for project in all_projects:
            print("Addding project %s" % project)
            if project == 'LCGCMT':
                print("Skipping project %s" % project)
                continue
            props = self.old_db.getProjectProperties(project)
            sourceUri = props.get('sourceuri', None)
            self.new_db.getOrCreateProjectNode(project, sourceuri=sourceUri)
        for platform in self.old_db.listAllPlatforms():
            print("Addding platform %s" % platform)
            node_platform = Platform(platform)
            self.new_db.mNeoDB.push(node_platform)
        used = self.old_db.listUsed()
        active = self.old_db.listActive()
        for project in all_projects:
            if project == 'LCGCMT':
                print("Skipping project %s" % project)
                continue
            for version in self.old_db.listVersions(project):
                print("Performing import for: %s %s" % (version[0], version[1]))
                buildTool = self.old_db.getBuildTools(version[0], version[1])
                parent = self.new_db.getOrCreatePV(version[0], version[1])
                sourceUri = self.old_db.getSourceURI(version[0], version[1])
                query = 'start n=node:ProjectVersion(ProjectVersion="%s_%s") match ' \
                        'p=n-[:REQUIRES]->m  return distinct m.project, ' \
                        'm.version' % (version[0], version[1])
                pvs = []
                self.old_db.runCypher(query, lambda x: pvs.append((x[0], x[1])))
                if len(buildTool):
                    self.new_db.setBuildTool(version[0], version[1],
                                             buildTool[0])
                if sourceUri:
                    self.new_db.setPVProperty(version[0], version[1],
                                              'sourceuri',
                                              sourceUri)
                for platform in self.old_db.listPlatforms(version[0],
                                                          version[1]):
                    print("=============Adding platform: %s" % (platform))
                    self.new_db.addPVPlatform(version[0], version[1], platform)

                for dep in pvs:
                    if dep[0] == 'LCGCMT':
                        dep = ('LCG', dep[1])
                    print("=============Adding dep: %s %s" % (dep[0],
                                                              dep[1]))

                    child = self.new_db.getOrCreatePV(dep[0], dep[1])
                    self.new_db.addRequires(parent, child)

                # Applay other props for pv.
                old_pvs_props = self.old_db.getPVProperties(version[0],
                                                            version[1])
                try:
                    new_pvs_props = self.new_db.getPVProperties(version[0],
                                                                version[1])
                    for key in old_pvs_props.keys():
                        if key not in new_pvs_props.keys():
                            self.new_db.setPVProperty(version[0], version[1],
                                                      key, old_pvs_props[key])
                    # used
                    if version in used:
                        print("=============Marking as used ")
                        self.new_db.setPVUsed(version[0], version[1])
                    # active
                    if version in active:
                        print("=============Marking as active ")
                        self.new_db.setPVActive(version[0], version[1])
                    # tags ?
                    # Set release date to today
                    self.new_db.setPVProperty(version[0], version[1],
                                              'releasedDate',
                                              str(datetime.now()))
                except Exception as e:
                    self.errors.append(version)

        print("Errors found in:")
        for error in self.errors:
            print(error)

    '''
    def start_APP_IMPORTER(self):
        all_projects = self.old_db.listProjects()
        for project in all_projects:
            print("Addding project %s" % project)
            props = self.old_db.getProjectProperties(project)
            sourceUri = props.get('sourceuri', None)
            self.new_db.getOrCreateProjectNode(project, sourceuri=sourceUri)
        for platform in self.old_db.listAllPlatforms():
            print("Addding platform %s" % platform)
            node_platform = Platform(platform)
            self.new_db.mNeoDB.push(node_platform)
        used = self.old_db.listUsed()
        active = self.old_db.listActive()
        for project in all_projects:
            for version in self.old_db.listVersions(project):
                print("Performing import for: %s %s" % (version[0], version[1]))
                buildTool = self.old_db.getBuildTools(version[0], version[1])
                if len(buildTool):
                    buildTool = buildTool[0]
                else:
                    buildTool = None
                try:

                    args = ['--norelease']
                    if buildTool:
                        args.append('--buildtool=%s' % buildTool.lower())
                    args.extend([version[0], version[1]])
                    s = LbSdbImportProject()
                    s.run(args=args)
                    for platform in self.old_db.listPlatforms(version[0],
                                                              version[1]):
                        s = LbSdbAddPlatform()
                        s.run(args=[version[0], version[1], platform])
                except Exception as e:
                    try:
                        self.errors_retry(version)
                    except Exception as e:
                        self.errors.append(version)
                # Applay other props for pv.
                old_pvs_props = self.old_db.getPVProperties(version[0],
                                                            version[1])
                try:
                    new_pvs_props = self.new_db.getPVProperties(version[0],
                                                                version[1])
                    for key in old_pvs_props.keys():
                        if key not in new_pvs_props.keys():
                            self.new_db.setPVProperty(version[0], version[1],
                                                      key, old_pvs_props[key])
                    # used
                    if version in used:
                        print("=============Marking as used ")
                        self.new_db.setPVUsed(version[0], version[1])
                    # active
                    if version in active:
                        print("=============Marking as active ")
                        self.new_db.setPVActive(version[0], version[1])
                    # tags ?
                    # Set release date to today
                    self.new_db.setPVProperty(version[0], version[1],
                                              'releasedDate',
                                              str(datetime.now()))
                except Exception as e:
                    self.errors.append(version)

        print("Errors found in:")
        for error in self.errors:
            print(error)

    def errors_retry(self, version):
        parent = self.new_db.getOrCreatePV(version[0], version[1])
        buildTool = self.old_db.getBuildTools(version[0], version[1])
        sourceUri = self.old_db.getSourceURI(version[0], version[1])
        query = 'start n=node:ProjectVersion(ProjectVersion="%s_%s") match ' \
                'p=n-[:REQUIRES]->m  return distinct m.project, ' \
                'm.version' % (version[0], version[1])
        pvs = []
        self.old_db.runCypher(query, lambda x: pvs.append((x[0], x[1])))
        if len(buildTool):
            self.new_db.setBuildTool(version[0], version[1], buildTool[0])
        if sourceUri:
            self.new_db.setPVProperty(version[0], version[1], 'sourceuri',
                                      sourceUri)
        for platform in self.old_db.listPlatforms(version[0],
                                                  version[1]):
            self.new_db.addPVPlatform(version[0], version[1], platform)

        for dep in pvs:
            child = self.new_db.getOrCreatePV(dep[0], dep[1])
            self.new_db.addRequires(parent, child)
    '''


def main():
    runner = LbSoftConfDbMigration()
    runner.start()


if __name__ == '__main__':
    main()