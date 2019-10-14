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
