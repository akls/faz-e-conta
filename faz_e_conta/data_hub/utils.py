from django.db.models import Q

def dynamic_filter(model, filters):
    """
    Generic filtering function for any Django model.

    :param model: The model class to filter (e.g., Aluno, DespesaFixa).
    :param filters: Dictionary of filter conditions (e.g., {"sala_id": 1, "nome__icontains": "John"}).
    :return: Queryset of filtered results.
    """
    query = Q()
    
    for field, value in filters.items():
        if value:  # Only apply filter if a value is provided
            query &= Q(**{field: value})

    return model.objects.filter(query)
