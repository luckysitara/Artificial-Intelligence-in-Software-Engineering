list_t *add_node_end(list_t *head, const int n) {
    list_t *new_node = malloc(sizeof(list_t));
    list_t *current = head;
    if (!head)
        return (new_node);
    while (current)
        current = current->next;
    current = new_node;
    new_node->n = n;
    new_node->next = NULL;
    return (head);
}
