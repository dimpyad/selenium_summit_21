from selenium import webdriver
import time
draw = '''
function drawStar(cx, cy, spikes, outerRadius, innerRadius) {
    var canvas = document.getElementById('canvas');
    var ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    var img = new Image();
    img.src = 'https://mdn.mozillademos.org/files/222/Canvas_createpattern.png';
    var pattern = ctx.createPattern(img, 'repeat');
    ctx.fillStyle = pattern;
    ctx.fillRect(0, 0, canvas.width, canvas.width);
    var rot = Math.PI / 2 * 3;
    var x = cx;
    var y = cy;
    var step = Math.PI / spikes;

    ctx.strokeSyle = "#000";
    ctx.beginPath();
    ctx.moveTo(cx, cy - outerRadius)
    for (i = 0; i < spikes; i++) {
        x = cx + Math.cos(rot) * outerRadius;
        y = cy + Math.sin(rot) * outerRadius;
        ctx.lineTo(x, y)
        rot += step

        x = cx + Math.cos(rot) * innerRadius;
        y = cy + Math.sin(rot) * innerRadius;
        ctx.lineTo(x, y)
        rot += step
    }
    ctx.lineTo(cx, cy - outerRadius)
    ctx.closePath();
    ctx.lineWidth=5;
    ctx.strokeStyle='DarkViolet';
    ctx.stroke();
    ctx.fillStyle='DarkKhaki';
    ctx.fill();

}
'''
message = '''
function write_text(text){
canvas = document.getElementById('canvas');
ctx = canvas.getContext('2d');
ctx.fillStyle='Cornsilk';
ctx.fillRect(0,0,canvas.width, canvas.height);
}
'''

inner_animation = '''
function innerShadow() {
  canvas = document.getElementById('canvas');
  ctx = canvas.getContext('2d');
  function drawShape() { // draw anti-clockwise
    ctx.arc(0, 0, 100, 0, Math.PI * 2, true); // Outer circle
    ctx.moveTo(70, 0);
    ctx.arc(0, 0, 70, 0, Math.PI, false); // Mouth
    ctx.moveTo(-20, -20);
    ctx.arc(30, -30, 10, 0, Math.PI * 2, false); // Left eye
    ctx.moveTo(140, 70);
    ctx.arc(-20, -30, 10, 0, Math.PI * 2, false); // Right eye
  };

  var width = 200;
  var offset = width + 50;
  var innerColor = "rgba(0,0,0,1)";
  var outerColor = "rgba(0,0,0,1)";

  ctx.translate(150, 170);

  // apply inner-shadow
  ctx.save();
  ctx.fillStyle = "#000";
  ctx.shadowColor = innerColor;
  ctx.shadowOffsetX = -15;
  ctx.shadowOffsetY = 15;

  // create clipping path (around blur + shape, preventing outer-rect blurring)
  ctx.beginPath();
  ctx.rect(-offset/2, -offset/2, offset, offset);
  ctx.clip();

  // apply inner-shadow (w/ clockwise vs. anti-clockwise cutout)
  ctx.beginPath();
  ctx.rect(-offset/2, -offset/2, offset, offset);
  drawShape();
  ctx.fill();
  ctx.restore();

  // cutout temporary rectangle used to create inner-shadow
  ctx.globalCompositeOperation = "destination-out";
  ctx.fill();

  // prepare vector paths
  ctx.beginPath();
  drawShape();

  // apply fill-gradient to inner-shadow
  ctx.save();
  ctx.globalCompositeOperation = "source-in";
  var gradient = ctx.createLinearGradient(-offset/2, 0, offset/2, 0);
  gradient.addColorStop(0.3, '#ff0');
  gradient.addColorStop(0.7, '#f00');
  ctx.fillStyle = gradient;
  ctx.fill();

  // apply fill-pattern to inner-shadow
  ctx.globalCompositeOperation = "source-atop";
  ctx.globalAlpha = 1;
  ctx.rotate(0.9);
  ctx.fill();
  ctx.restore();

  // apply fill-gradient
  ctx.save();
  ctx.globalCompositeOperation = "destination-over";
  var gradient = ctx.createLinearGradient(-offset/2, -offset/2, offset/2, offset/2);
  gradient.addColorStop(0.1, '#f00');
  gradient.addColorStop(0.5, 'rgba(255,255,0,1)');
  gradient.addColorStop(1.0, '#00f');
  ctx.fillStyle = gradient
  ctx.fill();

  // apply fill-pattern
  ctx.globalCompositeOperation = "source-atop";
  ctx.globalAlpha = 0.2;
  ctx.rotate(-0.4);
  ctx.fill();
  ctx.restore();

  // apply outer-shadow (color-only without temporary layer)
  ctx.globalCompositeOperation = "destination-over";
  ctx.shadowColor = outerColor;
  ctx.shadowBlur = 40;
  ctx.shadowOffsetX = 15;
  ctx.shadowOffsetY = 10;
  ctx.fillStyle = "#fff";
  ctx.fill();
  
  //Add text
  ctx.font = "30px Arial";
  ctx.strokeText("THANK YOU SO MUCH FOR WATCHING MAGIC WITH SELENIUM SESSION !!",100,200);
  };
'''

'''
This method will be using selenium execute javascript to create
some cool graphics/text on html canvas. We will be directly manipulate
the 2d context of html canvas to perform those operations.
'''
def draw_star():
    driver = webdriver.Chrome('./chromedriver')
    driver.maximize_window()
    driver.get("file:///Users/dimpya/MyAssistant/src/canvas.html")

    driver.execute_script(draw+" drawStar(100, 100, 5, 100, 15);")
    time.sleep(2)
    driver.execute_script(draw + " drawStar(1300, 100, 12, 100, 5);")
    time.sleep(2)
    driver.execute_script(draw + " drawStar(100, 500, 10, 100, 10);")
    time.sleep(2)
    driver.execute_script(draw + " drawStar(1300, 500, 20, 100, 20);")
    time.sleep(2)
    driver.execute_script(inner_animation + " innerShadow(); ")
    time.sleep(5)
    driver.close()

if __name__ == '__main__':
    draw_star()