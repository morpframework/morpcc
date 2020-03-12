from morpcc.crud.model import CollectionUI, ModelUI


class ApplicationModelUI(ModelUI):
    pass


class BehaviorableApplicationModelUI(ApplicationModelUI):
    def __new__(cls, request, model, collection):
        behaviors = model.behaviors()
        if not behaviors:
            return ApplicationModelUI(request, model, collection)

        markers = [behavior.modelui_marker for behavior in behaviors]
        markers.append(ApplicationModelUI)
        klass = type(
            "ApplicationModelUI", tuple(markers), {"__path_model__": ApplicationModelUI}
        )
        return klass(request, model, collection)


class ApplicationCollectionUI(CollectionUI):
    modelui_class = BehaviorableApplicationModelUI

    columns = [
        {"title": "Title", "name": "title"},
        {"title": "Description", "name": "description"},
        {"title": "Actions", "name": "structure:buttons"},
    ]
