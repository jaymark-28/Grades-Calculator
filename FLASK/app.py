from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def calculate_required_grades():
    passing_grade = 75
    prelim_weight = 0.20
    midterm_weight = 0.30
    final_weight = 0.50
    
    required_midterm_grade = 75
    required_final_grade = 75
    error = None
    
    if request.method == 'POST':
        try:
            prelim_grade = float(request.form['prelim_grade'])
            
            # Validate Prelim grade
            if not (0 <= prelim_grade <= 100):
                raise ValueError("Prelim grade must be 75 to pass.")
            
            # Calculate required Midterm and Final grades
            max_possible_midterm_final = (passing_grade - prelim_weight * prelim_grade) / (midterm_weight + final_weight)
            
            if max_possible_midterm_final < 0:
                error = "It's mathematically impossible to pass with the given Prelim grade."
            else:
                required_midterm_grade = max_possible_midterm_final
                required_final_grade = max_possible_midterm_final
            
        except ValueError as e:
            error = str(e)
        except TypeError as e:
            error = "Invalid type encountered: " + str(e)
    
    return render_template('index.html', required_midterm_grade=required_midterm_grade, required_final_grade=required_final_grade, error=error)

if __name__ == '__main__':
    app.run(debug=True)
