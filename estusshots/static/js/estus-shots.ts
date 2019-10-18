class EditorModule{

  setCurrentTime = (elemId: string) => {
    const elem = document.getElementById(elemId) as HTMLInputElement;
    if (!elem) return;
    elem.value = this.currentTimeHHMM()
  };

  currentTimeHHMM = () => {
    const d = new Date();
    const hours = (d.getHours()<10 ? '0' : '') + d.getHours();
    const minutes = (d.getMinutes()<10 ? '0' : '') + d.getMinutes();
    return `${hours}:${minutes}`;
  };
}

const editorModule = new EditorModule();

interface HTMLElement {
    addClass(cssClass: string): void;
    removeClass(cssClass: string): void;
}

HTMLElement.prototype.addClass = function(cssClass: string): void {
  if (!this.classList.contains(cssClass)){
    this.classList.add(cssClass);
  }
};
HTMLElement.prototype.removeClass = function(cssClass: string): void {
  if (this.classList.contains(cssClass)){
    console.log(this.classList);
    this.classList.remove(cssClass);
  }
};

namespace EventEditor {

  export let updateControls = () => {
    const typeSelect = document.getElementById("event_type") as HTMLSelectElement;
    const selectedType = typeSelect.options[typeSelect.selectedIndex].value;

    const penalties = document.querySelector(".penalty-container") as HTMLDivElement;
    const player = document.getElementById("player_row") as HTMLDivElement;
    const enemy = document.getElementById("enemy_row") as HTMLDivElement;

    switch (selectedType) {
      // Pause
      case "0":
        penalties.addClass("d-none");
        player.addClass("d-none");
        enemy.addClass("d-none");
        break;
        // Death
        case "1":
          penalties.removeClass("d-none");
          player.removeClass("d-none");
          enemy.removeClass("d-none");
          break;
        // Victory
        case "2":
          penalties.addClass("d-none");
          player.removeClass("d-none");
          enemy.removeClass("d-none");
          break;
    }
  }

}
