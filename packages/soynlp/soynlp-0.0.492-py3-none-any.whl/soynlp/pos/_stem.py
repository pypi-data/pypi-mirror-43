# -*- encoding:utf8 -*-

def conjugate_exception(v, e):
    v_ = decompose(v[-1])
    e_ = decompose(e[0])
    e_2 = compose(e_[0], e_[1], ' ')
    
    # 르 불규칙 활용 예외
    if (v[-1] == '치' and e_2 == '러'):
        return (v, e)
    if (v[-1] == '들' and e_2 == '러'):
        return (v, e)
    if v[-2:] == '다다' and e_2 == '라':
        return (v, e)

def conjugate(v, e):
    # Develop code
    verbs = {
        '깨닫', '불', '묻', '눋', '겯', '믿', '묻', '뜯', # ㄷ 불규칙
        '구르', '무르', '마르', '누르', '나르', '모르', '이르', # 르 불규칙
        '아니꼽', '우습', '더럽', '아름답', '잡', '뽑', '곱', '돕', # ㅂ 불규칙
        '낫', '긋', '붓', '뭇', '벗', '솟', '치솟', '씻', '손씻', '뺏', # ㅅ 불규칙
        '똥푸', '주',  # 우 불규칙
        '끄', '크', '트', # ㅡ 탈락 불규칙
        '삼가', '가', '들어가', # 거라 불규칙
        '돌아오', '오', # 너라 불규칙
        '이르', '푸르', '누르', # 러 불규칙
        '하', '노랗', '퍼렇', '놀라' # 여 불규칙
    }

    eomis = {
        '아', '어나다', '어', '워', '웠다', '워서', '왔다', '와주니', '었다', '었어', '았어', '데', 
        '라', '라니까', '너라', '았다', '러'
    }

    def is_verb(w): return w in verbs
    def is_eomi(w): return w in eomis
    
    # https://namu.wiki/w/한국어/불규칙%20활용
    
    if (v and e) and (is_verb(v) and is_eomi(e)):
        return (v, e)
    
    vl = v[-1]
    ef = e[0] if e else ' '
    v_ = decompose(vl)
    v_2 = compose(v_[0], v_[1], ' ')
    e_ = decompose(ef) if e else (' ', ' ', ' ')
    e_2 = compose(e_[0], e_[1], ' ') if e else ' '
        
    ## 1. 어간이 바뀌는 불규칙 활용
    # 1.1. ㄷ 불규칙 활용: 깨닫 + 아 -> 꺠달아
    if (v_[2] == 'ㄹ') and (e_[0] == 'ㅇ'):
        canonicalv = v[:-1] + compose(v_[0], v_[1], 'ㄷ')
        if is_verb(canonicalv) and is_eomi(e):
            return (canonicalv, e)
    
    # 1.2. 르 불규칙 활용
    if (v_[2] == 'ㄹ') and (e_2 == '러' or (e_2 == '라')):
        canonicalv = v[:-1] + compose(v_[0], v_[1], ' ') + '르'
        canonicale = '어' + e[1:]
        if is_verb(canonicalv) and is_eomi(canonicale):
            return (canonicalv, canonicale)

    # 1.3. ㅂ 불규칙 활용
    if (v_[2] == ' ') and (e_2 == '워'):
        canonicalv = v[:-1] + compose(v_[0], v_[1], 'ㅂ')
        if is_verb(canonicalv) and is_eomi(e):
            return (canonicalv, e)
    
    if (v == '도' or v == '고') and (e_2 == '와'):
        canonicalv = compose(v_[0], v_[1], 'ㅂ')
        if is_verb(canonicalv) and is_eomi(e):
            return (canonicalv, e)
    
    # 1.4. ㅅ 불규칙 활용
    if (v_[2] == ' ') and (e_[0] == 'ㅇ'):
        canonicalv = v[:-1] + compose(v_[0], v_[1], 'ㅅ')
        if is_verb(canonicalv) and is_eomi(e):
            return (canonicalv, e)
    
    # 1.5. 우 불규칙 활용
    # 드러눕 + 어 -> (드러누어) -> 드러눠 -> 드러눠
    if v_2 == '퍼':
        if e == '': return (v[:-1] + '푸', '어')        
        return (v[:-1] + '푸', compose('ㅇ', 'ㅓ', e_[2]) + e[1:])
    
    if v_[1] == 'ㅝ':
        canonicalv = v[:-1] + compose(v_[0], 'ㅜ', ' ')
        if is_verb(canonicalv) and ((not e) or is_eomi(e)):
            return (canonicalv, compose('ㅇ', 'ㅓ', v_[2]) + ('' if not e else e[1:]))
    
    # 1.6. ㅡ 탈락 불규칙 활용
    if (v_[1] == 'ㅓ' or v_[1] == 'ㅏ'):
        canonicalv = v[:-1] + compose(v_[0], 'ㅡ', ' ')
        if is_verb(canonicalv) and ((not e) or is_eomi(e)):
            return (canonicalv, compose('ㅇ', 'ㅓ', v_[2]) + e)
    
    ## 2. 어미가 바뀌는 불규칙 활용
    # 2.1. 거라 불규칙 활용
    if (vl == '가') and (e and (e[0] == '라' or e[:2] == '거라')):
        canonicale = '' if not e else (e[1:] if e[0] == '거' else e)
        if is_verb(vl) and is_eomi(canonicale):
            return (vl, canonicale)
    
    # 2.2. 너라 불규칙 활용
    # 돌아오 + -너라 = 돌아오너라, 돌아오 + 라고 = 돌아오라고: 규칙임
    # 2.2-2: 돌아오다 + 았다 -> 돌아왔다
    if (v_[1] == 'ㅘ'):
        canonicalv = v[:-1] + compose(v_[0], 'ㅗ', ' ')
        canonicale = compose('ㅇ', 'ㅏ', v_[2]) + e
        if is_verb(canonicalv) and is_eomi(canonicale):
            return (canonicalv, canonicale)
    
    # 2.3. 러 불규칙 활용
    if (e_[0] == 'ㄹ' and e_[1] == 'ㅓ'):
        canonicale = compose('ㅇ', 'ㅓ', e_[2]) + e[1:]
        if is_verb(v) and is_eomi(canonicale):
            return (v, canonicale)
    
    # 2.4. 여 불규칙 활용
    # 하 + 았다 -> 하였다: '였다'를 어미로 넣으면 되는 문제
    
    # 2.5. 오 불규칙 활용
    # 달 + 아라 -> 다오, 걸 + 어라 -> 거오: 문어체적 표현에 자주 등장하며 구어체에서는 거의 없음
    # 생략
    
    ## 3. 어간과 어미가 모두 바뀌는 불규칙 활용
    # 3.1. ㅎ 불규칙 활용
    
    # (추가) 3.2 어미가 ㄴ인 경우: 조사가 ㄴ / ㄹ인 경우 역시 명사 추출 단에서 해야 함
    if (not e) and (v_[2] == 'ㄴ' or v_[2] == 'ㄹ'):
        canonicalv = v[:-1] + compose(v_[0], v_[1], ' ')
        if is_verb(canonicalv):
            return (canonicalv, v_[2])
        # 노랗 + ㄴ -> 노란
        canonicalv = v[:-1] + compose(v_[0], v_[1], 'ㅎ')
        if is_verb(canonicalv):
            return (canonicalv, v_[2])
        
    # 4. 활용이 불완전한 동사
    
    
    ## 5. 헷갈리기 쉬운 불규칙 활용
    # 5.1. 이르다
    
    
    # 5.2. 붇다, 붓다, 불다
    
    
    ## 6. 체언    
    # 6.1. 복수형
    
    
    ## 7. 높임법
    # 7.1. 조사
    
    
    return (v, e)