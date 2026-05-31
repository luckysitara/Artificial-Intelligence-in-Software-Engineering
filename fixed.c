list_t *add_node_end(list_t **head, const int n)
{
    list_t *new_node;
    list_t *current;

    /* Always check malloc's return value — it returns NULL on failure */
    new_node = malloc(sizeof(list_t));
    if (!new_node)
        return (NULL);

    /* Initialize the new node's fields BEFORE linking it anywhere */
    new_node->n    = n;
    new_node->next = NULL;  /* This node will be the new tail */

    /* If the list is empty, the new node simply becomes the head */
    if (!(*head))
    {
        *head = new_node;
        return (new_node);
    }

    /* 
     * Traverse to the LAST node, not past it.
     * Condition is current->next != NULL so we stop
     * while current still points at the final node.
     */
    current = *head;
    while (current->next)
        current = current->next;

    /* Now current IS the last node — link new_node in */
    current->next = new_node;

    return (new_node);  /* Return the new node (useful for the caller) */
}
