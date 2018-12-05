var RightClick = {
	init: function () {
	    this.FlashObjectID = "flashMovie";
		this.FlashContainerID = "media";
		this.Cache = this.FlashObjectID;
		document.getElementById(this.FlashContainerID).onmouseup = function() 
		{ 
		    document.getElementById(RightClick.FlashContainerID).releaseCapture(); 
        }
        document.oncontextmenu = function()
		{ 
		    if(window.event.srcElement.id == RightClick.FlashObjectID) 
		    { 
		        return false; 
		    } 
		    else 
		    { 
		        RightClick.Cache = "nan"; 
		    }
        }
        document.getElementById(this.FlashContainerID).onmousedown = RightClick.onIEMouse;
	},
	onIEMouse: function() {
	  	if (event.button > 1) {
			if(window.event.srcElement.id == RightClick.FlashObjectID && RightClick.Cache == RightClick.FlashObjectID) {
				RightClick.call(); 
			}
			document.getElementById(RightClick.FlashContainerID).setCapture();
			if(window.event.srcElement.id)
			RightClick.Cache = window.event.srcElement.id;
		}
	}
}