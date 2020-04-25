import csv

# Global bird variables

original_colors = [(189, 208, 196), # Green
          (154,183,211), # Blue
          (245,210,211), # Red
          (247,225,211), # Brown
          (243,209,165) # Gold
          ]

beach_pastel_colors = [
          (233, 189, 176),
          (246, 221, 208),
          (236, 234, 229),
          (185, 222, 219),
          (137, 199, 203)
          ]

parrot_colors = [
                 (207, 144, 51),
                 (189, 99, 37),
                 (128, 26, 25),
                 (68, 96, 118),
                 (39, 45, 23)
                 ]

blue_and_brown_colors = [
                         (175, 190, 189),
                         (225, 219, 209),
                         (212, 179, 148),
                         (180, 150, 149),
                         (168, 191, 178)
                         ]

shades_of_green_colors = [
                          (107, 125, 128),
                          (133, 158, 163),
                          (159, 180, 177),
                          (186, 197, 193),
                          (198, 203, 189)
                          ]

green_and_gold_colors = [
                         (206, 175, 78),
                         (220, 193, 105),
                         (134, 168, 113),
                         (110, 152, 80)
                         ]

royal_colors = [
              (187, 59, 52),
              (235, 175, 61),
              (204, 145, 50),
              (49, 65, 138)
              ]

gold_gradient_colors = [
                        (224, 202, 153),
                        (168, 133, 47),
                        (151, 118, 42),
                        (176, 150, 83)
                        ]


greenish_blue_with_orange = [
                             (46, 107, 141),
                             (229, 146, 53),
                             (180, 201, 214),
                             (161, 191, 94),
                             (101, 184, 215)
                             ]

pale_beachy = [
               (180, 207, 201),
               (223, 219, 231),
               (213+10, 176+30, 92+30),
               (157, 178, 206)
               ]

background_color = (255, 255, 255)
w, h = 164 * 8, 164 * 8

def setup():
    
    # Number of birds
    grid_x = 10
    grid_y = 9
    
    # The birds will draw inside this rectangle
    grid_x_pixels = .8 * w
    grid_y_pixels = .8 * h
    
    scale_factor = 0.45

    size(w, h)
    
    background(*background_color)
    pixelDensity(2)
    stroke(0)
    strokeWeight(scale_factor * 7)
    strokeJoin(ROUND)
    
    colors = pale_beachy
    gray_color = (100, 100, 100)
    black_color = (0,0,0)
    feet_eye_color = gray_color
    
    name_table = loadTable("Bird_Names.csv", "header")
    names = []
    for name in name_table.rows(): names.append(name.getString("name"))
    f_kokonor = loadFont("Kokonor-18.vlw")
    f_avenir = loadFont("Avenir-Light-12.vlw")
    textFont(f_kokonor)
    textAlign(CENTER, CENTER)
    textSize(12)
        
    drawBirds(w, h, grid_x_pixels, grid_y_pixels, grid_x, grid_y, colors, names, feet_eye_color, scale_factor)
            
    seed = str(int(random(10000)))
    save("Examples/" + str(grid_x) + "-" + str(grid_y) + "-s-" + seed + ".png")

def clearBirds():
    background(*background_color)

def mouseReleased():
    clearBirds()
    drawBirds()

################
## Draw Birds ##
################

def drawBirds(w, h, grid_x_pixels, grid_y_pixels, grid_x, grid_y, colors, names, feet_eye_color, scale_factor):
    current_x = w/2.0 - grid_x_pixels/2.0
    current_y = h/2.0 - grid_y_pixels/2.0 + scale_factor * 100
    
    # Distance between the birds
    sep_x = grid_x_pixels / (grid_x - 1)
    sep_y = grid_y_pixels / (grid_y - 1)
    
    for i in range(grid_x):
        for j in range(grid_y):
            
            fill_color = get_random_element(colors)
            inc = .2 * 255
            stroke_color = (fill_color[0] - inc, fill_color[1] - inc, fill_color[2] - inc)
            name = names.pop()
            bird = Bird(name, current_x, current_y, fill_color, stroke_color, feet_eye_color, background_color, scale_factor)
            draw_bird(bird)

            current_y += sep_y
        current_y = h/2.0 - grid_y_pixels/2.0 + scale_factor * 100
        current_x += sep_x

def draw_bird(bird):

    draw_legs(bird.legs)
    draw_body(bird.body)
    
    if (bird.has_tail): draw_tail(bird.tail)
        
    draw_beak(bird.beak)
    draw_head(bird.head)
    draw_eye(bird.eye)
    draw_name(bird.name_point, bird.name, bird.feet_eye_color)
    
def draw_name(name_point, name, text_color):
    fill(*text_color)
    text(name, name_point['x'], name_point['y'])

def draw_body(body):
    draw_shape(body.stroke_color, background_color, body.body_outline)
    for pts in body.body_accents:
        draw_shape(body.stroke_color, body.fill_color, pts)

def draw_legs(legs):
    draw_lines(legs.leg_color, legs.leg_lines[0], legs.leg_lines[1], legs.leg_lines[2])

def draw_tail(tail):
    draw_shape(tail.stroke_color, tail.fill_color, [
                                                    (tail.tail_extents[0]['x'], tail.tail_extents[0]['y']),
                                                    (tail.tail_extents[1]['x'], tail.tail_extents[1]['y']),
                                                    (tail.tail_extents[2]['x'], tail.tail_extents[2]['y']),
                                                    (tail.tail_extents[3]['x'], tail.tail_extents[3]['y']),
                                                    ])        

def draw_eye(birdEye):
    draw_circle(birdEye.iris_color, birdEye.outline_color, birdEye.eye_center[0], birdEye.eye_center[1], birdEye.eye_size)
    draw_circle(birdEye.pupil_color, birdEye.pupil_color, birdEye.eye_center[0], birdEye.eye_center[1], birdEye.eye_thickness, False)

def draw_beak(beak):
    draw_triangle(beak.fill_color, beak.stroke_color, 
            beak.beak_top['x'], beak.beak_top['y'], 
            beak.beak_bottom['x'], beak.beak_bottom['y'], 
            beak.beak_extent['x'], beak.beak_extent['y'])

def draw_head(head):
    draw_circle(background_color, head.stroke_color,head.center['x'], head.center['y'], head.head_size)
    draw_PIE_arc(head.fill_color, head.center['x'], head.center['y'], head.head_size, head.head_size, head.arc_min, head.arc_max)
    draw_circle(head.fill_color, head.stroke_color, head.center['x'], head.center['y'], head.head_size, True, False)


##################
## Bird Classes ##
##################

class Bird:
    def __init__(self, name, location_x, location_y, fill_color, stroke_color, feet_eye_color, background_color, scale_factor):
        self.name = name
        self.name_point = {'x': location_x, 'y': location_y + scale_factor * 40}
        self.legs = Legs({'x':location_x, 'y': location_y}, feet_eye_color, scale_factor)
        self.body = Body({'x': location_x, 'y': location_y}, fill_color, stroke_color, scale_factor)
        self.head = Head(location_x, location_y, self.body.body_height, fill_color, stroke_color, scale_factor)
        self.beak = Beak(self.head.center['x'], self.head.center['y'], self.head.head_size, background_color, fill_color, stroke_color, scale_factor)
        self.eye = Eye(self.head.center['x'], self.head.center['y'], self.head.head_size, background_color, feet_eye_color, stroke_color, scale_factor)
        self.has_tail = self.body.has_tail
        if(self.has_tail): self.tail = Tail({ 'x': self.body.body_outline[0][0], 'y': self.body.body_outline[0][1]}, stroke_color, fill_color, scale_factor)
        self.feet_eye_color = feet_eye_color
        
class Body:
    def __init__(self, base_point, fill_color, stroke_color, scale_factor):
        self.stroke_color = stroke_color
        self.fill_color = fill_color
        
        offset = scale_factor * 40
        x = base_point['x']
        y = base_point['y']
        
        feet_length = scale_factor * 40
        body_height = scale_factor * 100
        body_bottom = y - feet_length/2.0
    
        body_one = (int(x - feet_length * 2.0), int(body_bottom))
        body_two = (int(x + feet_length*1.5), int(body_bottom))
        body_three = (int(x + feet_length*2.1), int(body_bottom - body_height))
        body_four = (int(x), int(body_bottom - body_height * 1.3))
        
        left_midpoint = ((body_four[0] + body_one[0]) / 2, (body_four[1] + body_one[1]) / 2)
        top_midpoint = ((body_four[0] + body_three[0]) / 2, (body_four[1] + body_three[1]) / 2)
        right_midpoint = ((body_two[0] + body_three[0]) / 2, (body_two[1] + body_three[1]) / 2)
        bottom_midpoint = ((body_one[0] + body_two[0]) / 2, (body_one[1] + body_two[1]) / 2)
        
        true_midpoint = ((left_midpoint[0] + right_midpoint[0]) / 2, (left_midpoint[1] + right_midpoint[1]) / 2)
        
        body_points = [ body_one, body_two, body_three, body_four, left_midpoint, top_midpoint, bottom_midpoint]
        
        self.body_outline = [body_one, body_two, body_three, body_four]
        self.body_accents = []
        for i in range(int(random(1, 4))):
            point_one = get_random_element(body_points)
            point_two = get_random_element(body_points)
            point_three = get_random_element(body_points)
            self.body_accents.append([point_one, point_two, point_three])
        self.body_height = body_height
        
        tail_chance = 0.7
        self.has_tail = random(1) < tail_chance

class Legs:
    def __init__(self, body_location, feet_color, scale_factor):
        feet_length = scale_factor * 40
        
        x = body_location['x']
        y = body_location['y']
        
        line1 = (int(x - feet_length), int(y), int(x + feet_length), int(y))
        line2 = (int(x - feet_length/3.0), int(y), int(x - feet_length/3.0 - feet_length/2.0), int(y - feet_length))
        line3 = (int(x + feet_length/3.0), int(y), int(x + feet_length/3.0 - feet_length/2.0), int(y - feet_length))
        
        self.leg_color = feet_color
        self.leg_lines = [line1, line2, line3]
    
class Tail:
    def __init__(self, body_LL, stroke_color, fill_color, scale_factor):
        
        min_tail_width = scale_factor * 25
        max_tail_width = scale_factor * 40
        
        min_tail_x = scale_factor * -45
        max_tail_x = scale_factor * -15
        
        min_tail_y = scale_factor * -70
        max_tail_y = scale_factor * -30
        
        var_width = random(min_tail_width, max_tail_width)
        var_x = random(min_tail_x, max_tail_x)
        var_y = random(min_tail_y, max_tail_y)
        
        if(random(1) < 0.3): var_y *= -1
        
        self.tail_extents = [ { 'x': body_LL['x'], 'y': body_LL['y'] },
                             { 'x': body_LL['x'] + var_width, 'y': body_LL['y'] },
                             { 'x': body_LL['x'] + var_width + var_x, 'y': body_LL['y'] + var_y },
                             { 'x': body_LL['x'] + var_x, 'y': body_LL['y'] + var_y }
                             ]
        
        self.fill_color = fill_color
        self.stroke_color = stroke_color


class Head:
    def __init__(self, body_x, body_y, body_height, fill_color, stroke_color, scale_factor):
        head_offset_x = scale_factor * 40
        head_offset_y = -(head_offset_x/2.0 + body_height * 1.1)
        self.center = {'x': body_x + head_offset_x, 'y': body_y + head_offset_y}
        self.head_size = scale_factor * 90
        head_fill_value = random(1)
        empty_chance = 0.3
        arc_chance = 0.6
        
        if(head_fill_value <= empty_chance):
            self.arc_min = 0
            self.arc_max = 2 * PI
        elif(head_fill_value < arc_chance):
            self.arc_min = random(.7, 1)*PI
            self.arc_max = 1.8*PI
        else:
            self.arc_min = 0
            self.arc_max = 0
            
        self.fill_color = fill_color
        self.stroke_color = stroke_color
        

class Beak:
    def __init__(self, head_x, head_y, head_size, background_color, fill_color, stroke_color, scale_factor):
        self.stroke_color = stroke_color
        
        min_beak_size = scale_factor * 10
        max_beak_size = head_size * 0.5

        min_beak_length = scale_factor * 60
        max_beak_length = scale_factor * 100
        
        y_variance = random(min_beak_size, max_beak_size)
        length_variance = random(min_beak_length, max_beak_length)
        
        self.beak_top = {'x': head_x, 'y': head_y + y_variance}
        self.beak_bottom = {'x': head_x, 'y': head_y - y_variance}
        self.beak_extent = {'x': head_x + length_variance, 'y': head_y}
        
        filled_percent = 0.7
        self.fill_color = fill_color if random(1) < filled_percent else background_color

    
class Eye:
    def __init__(self, head_x, head_y, head_size, background_color, pupil_color, stroke_color, scale_factor):
        self.eye_center = (head_x + head_size/6.0, head_y - head_size/8.0)
        self.eye_size = scale_factor * 30
        self.eye_thickness = scale_factor * 12
        self.iris_color = background_color
        self.pupil_color = pupil_color
        self.outline_color = stroke_color  
    
#################
## Draw Shapes ##
#################

def draw_shape(stroke_color, fill_color, points_list):
    stroke(*stroke_color)
    fill(*fill_color)
    beginShape()
    for vert in points_list:
        vertex(*vert)
    endShape(CLOSE)

def draw_lines(line_color, *args):
    stroke(*line_color)
    strokeCap(ROUND)
    for myline in args:
        line(*myline)
    
def draw_triangle(interior_color, outline_color, x1, y1, x2, y2, x3, y3):
    stroke(*outline_color)
    fill(*interior_color)
    triangle(x1, y1, x2, y2, x3, y3)
    
def draw_circle(interior_color, outline_color, x, y, diameter, add_stroke=True, add_fill=True):
    if(add_stroke):
        stroke(*outline_color)
    else:
        noStroke()
    if(add_fill): 
        fill(*interior_color)
    else:
        noFill()
    circle(x, y, diameter)
    
def draw_PIE_arc(fill_color, x, y, wid, hei, start, stop):
    fill(*fill_color)
    noStroke()
    arc(x, y, wid, hei, start, stop, PIE)


## Utility

def get_random_element(l):
    return l[int(random(len(l)))]

    
    
    
    
    
    
    
    
    
    
    
    
    
