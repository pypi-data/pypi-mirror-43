class BaseObject(object):
    id = ""
    name = ""

    def __init__(self, object):
        self.id = object['id']
        self.name = object['name']


class Category(BaseObject):
    parent_id = ""
    client_id = ""
    deleted = False

    def __init__(self, category):
        super().__init__(category)
        self.client_id = category['clientId']
        self.parent_id = category['parentId']
        self.deleted = category['deleted']

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'parentId': self.parent_id,
            'clientId': self.client_id,
            'deleted': self.deleted
        }


class Automaton(BaseObject):
    category_id = ""
    client_id = ""
    template = False
    archived = False
    deleted = False

    def __init__(self, automaton):
        super().__init__(automaton)
        self.category_id = automaton['categoryId']
        self.client_id = automaton['clientId']
        self.deleted = automaton['deleted']
        self.template = automaton['template']
        self.archived = automaton['archived']

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'categoryId': self.category_id,
            'clientId': self.client_id,
            'template': self.template,
            'archived': self.archived,
            'deleted': self.deleted
        }


class ExportedAutomaton(BaseObject):
    automatonConnectionGroups = []
    automatonFlow = {}
    categoryPath = ""
    clientCode = ""
    creatorId = ""
    creatorName = ""
    designerDiagram = ""
    equivalentEngineerTime = 0.0
    executionMode = ""
    linkedAutomatons = []
    matcherDsl = ""
    newExecutionThrottleCount = 0
    newExecutionThrottlePeriodSeconds = 0
    notes = ""
    purpose = ""
    tags = []
    template = False
    versionId = 0
    versionNumber = 0

    def __init__(self, automaton):
        super().__init__(automaton)
        self.automatonConnectionGroups = automaton['automatonConnectionGroups']
        self.automatonFlow = automaton['automatonFlow']
        self.categoryPath = automaton['categoryPath']
        self.clientCode = automaton['clientCode']
        self.creatorId = automaton['creatorId']
        self.creatorName = automaton['creatorName']
        self.designerDiagram = automaton['designerDiagram']
        self.equivalentEngineerTime = automaton['equivalentEngineerTime']
        self.executionMode = automaton['executionMode']
        self.linkedAutomatons = automaton['linkedAutomatons']
        self.matcherDsl = automaton['matcherDsl']
        self.newExecutionThrottleCount = automaton['newExecutionThrottleCount']
        self.newExecutionThrottlePeriodSeconds = automaton['newExecutionThrottlePeriodSeconds']
        self.notes = automaton['notes']
        self.purpose = automaton['purpose']
        self.tags = automaton['tags']
        self.template = automaton['template']
        self.versionId = automaton['versionId']
        self.versionNumber = automaton['versionNumber']

    def json(self):
        return {
            'automatonConnectionGroups': self.automatonConnectionGroups,
            'automatonFlow': self.automatonFlow,
            'categoryPath': self.categoryPath,
            'clientCode': self.clientCode,
            'creatorId': self.creatorId,
            'creatorName': self.creatorName,
            'designerDiagram': self.designerDiagram,
            'equivalentEngineerTime': self.equivalentEngineerTime,
            'executionMode': self.executionMode,
            'linkedAutomatons': self.linkedAutomatons,
            'matcherDsl': self.matcherDsl,
            'newExecutionThrottleCount': self.newExecutionThrottleCount,
            'newExecutionThrottlePeriodSeconds': self.newExecutionThrottlePeriodSeconds,
            'notes': self.notes,
            'purpose': self.purpose,
            'tags': self.tags,
            'template': self.template,
            'versionId': self.versionId,
            'versionNumber': self.versionNumber,
        }


# Node Structure of K-ary Tree
class Node:

    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.children = []
        self.path = ""
