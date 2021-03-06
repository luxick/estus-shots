var EditorModule = (function () {
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
HTMLElement.prototype.addClass = function (cssClass) {
    if (!this.classList.contains(cssClass)) {
        this.classList.add(cssClass);
    }
};
HTMLElement.prototype.removeClass = function (cssClass) {
    if (this.classList.contains(cssClass)) {
        console.log(this.classList);
        this.classList.remove(cssClass);
    }
};
var EventEditor;
(function (EventEditor) {
    EventEditor.updateControls = function () {
        var typeSelect = document.getElementById("event_type");
        var selectedType = typeSelect.options[typeSelect.selectedIndex].value;
        var penalties = document.querySelector(".penalty-container");
        var player = document.getElementById("player_row");
        var enemy = document.getElementById("enemy_row");
        switch (selectedType) {
            case "0":
                penalties.addClass("d-none");
                player.addClass("d-none");
                enemy.addClass("d-none");
                break;
            case "1":
                penalties.removeClass("d-none");
                player.removeClass("d-none");
                enemy.removeClass("d-none");
                break;
            case "2":
                penalties.addClass("d-none");
                player.removeClass("d-none");
                enemy.removeClass("d-none");
                break;
        }
    };
})(EventEditor || (EventEditor = {}));
//# sourceMappingURL=estus-shots.js.map