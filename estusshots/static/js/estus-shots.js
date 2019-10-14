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
//# sourceMappingURL=estus-shots.js.map