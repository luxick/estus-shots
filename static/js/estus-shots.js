var EditorModule = /** @class */ (function () {
    function EditorModule() {
        var _this = this;
        this.setCurrentTime = function (elemId) {
            var elem = document.getElementById(elemId);
            if (!elem)
                return;
            elem.value = _this.currentTimeHHMM();
        };
        this.currentTimeHHMM = function () {
            var d = new Date();
            var hours = (d.getHours() < 10 ? '0' : '') + d.getHours();
            var minutes = (d.getMinutes() < 10 ? '0' : '') + d.getMinutes();
            return hours + ":" + minutes;
        };
    }
    return EditorModule;
}());
var editorModule = new EditorModule();
var EventEditor;
(function (EventEditor) {
    EventEditor.updateControls = function () {
        var typeSelect = document.getElementById("event_type");
        var selectedType = typeSelect.options[typeSelect.selectedIndex].value;
        switch (selectedType) {
            case "0":
                console.log("Pause");
                break;
            case "1":
                break;
            case "2":
                break;
            default:
                console.log("Unknown event type: " + selectedType);
        }
    };
})(EventEditor || (EventEditor = {}));
