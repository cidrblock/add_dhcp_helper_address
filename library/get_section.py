#!/usr/bin/env python
'''
Ansible module to snip a section from a configuration.
'''
# pylint: disable=redefined-builtin
from ansible.module_utils.basic import AnsibleModule
# pylint: enable=redefined-builtin
from ciscoconfparse import CiscoConfParse

def find_sections(**kwargs):
    """Extract a section from a config

    Args:
        lines (list): the list of lines making up the config
        match (str): the regex to match against
        child_match (str): the regex to match children against
        only_child_matches (boolean): only return sections with children that match
        min_child_lines (int): only return section that >= this many children

    Returns:
        dict: A dict of the sections, lines
    """
    parse = CiscoConfParse(kwargs['lines'])
    if kwargs['child_match'] == 'any':
        found_objs = parse.find_objects(kwargs['match'])
    else:
        if kwargs['children_that_match']:
            found_objs = parse.find_objects_w_child(parentspec=r"%s" % kwargs['match'], \
                childspec=r"%s" % kwargs['child_match'])
        else:
            found_objs = parse.find_objects_wo_child(parentspec=r"%s" % kwargs['match'], \
                childspec=r"%s" % kwargs['child_match'])

    found_objs = [obj for obj in found_objs if len(obj.children) >= kwargs['min_child_lines']]
    response = {}
    response['sections'] = []
    response['lines'] = []
    for section in found_objs:
        entry = {}
        entry['section_name'] = section.text
        response['lines'].append(section.text)
        entry['section_content'] = []
        for child in section.children:
            entry['section_content'].append(child.text.strip())
            response['lines'].append(child.text)
        response['sections'].append(entry)
    return response

def main():
    """ The main entry point

    Args:
        lines (list): the list of lines making up the config
        match (str): the regex to match against
        child_match (str): the regex to match children against
        only_child_matches (boolean): only return sections with children that match
        min_child_lines (int): only return section that >= this many children
    Returns:
        sections (list): A list of sections with name and content

    """
    module = AnsibleModule(
        argument_spec=dict(
            lines=dict(required=True, type='list'),
            match=dict(required=True, type='str'),
            child_match=dict(required=True, type='str'),
            children_that_match=dict(required=True, type='bool'),
            min_child_lines=dict(required=True, type='int')
        ),
        supports_check_mode=True)

    try:
        response = find_sections(lines=module.params['lines'],
                                 match=module.params['match'],
                                 child_match=module.params['child_match'],
                                 children_that_match=module.params['children_that_match'],
                                 min_child_lines=module.params['min_child_lines'])

        module.exit_json(changed=False, matches=response)

# pylint: disable=broad-except
    except Exception, error:
        error_type = error.__class__.__name__
        module.fail_json(msg=error_type + ": " + str(error))

if __name__ == "__main__":
    main()
